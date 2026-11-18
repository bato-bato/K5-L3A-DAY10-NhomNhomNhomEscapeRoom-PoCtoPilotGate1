"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    if order and order["customer_id"] == ctx.ticket.get("customer_id"):
        if any(p.get("status") == "DELIVERED" and not p.get("delivered_date")
               for p in order.get("parcels", ())):
            ctx.log("missing_delivery_date")
            return Verdict.escalate("delivered parcel has no recorded delivery date")
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action["tool"]
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier", "send_reply"):
        return Verdict.allow()

    if tool == "send_reply":
        proposal = next((e for e in ctx.events if e["type"] == "proposal"), None)
        if not proposal or proposal["amount_vnd"] > 0:
            return Verdict.allow()
    payload = action.get("payload", {})
    order_id = action.get("order_id") if tool != "notify_carrier" else payload.get("order_id")
    if tool == "send_reply":
        order_id = ctx.ticket.get("order_id")
    if not order_id or order_id != ctx.ticket.get("order_id"):
        return Verdict.deny("lệnh ghi không khớp đơn trên ticket")

    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not order.get("parcels") or policy is None:
        return Verdict.deny("thiếu dữ liệu đơn, kiện hoặc chính sách hiệu lực")

    requested_parcel = ctx.ticket.get("parcel_id")
    if requested_parcel and not any(p["parcel_id"] == requested_parcel for p in order["parcels"]):
        return Verdict.deny("kiện trên ticket không thuộc đơn")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)

    if tool in ("issue_refund", "send_reply"):
        entitlement = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if tool == "send_reply":
            if entitlement > 0 and proposal["delay_days_used"] != delay:
                return Verdict.escalate("negative refund decision conflicts with tracking")
            return Verdict.allow()
        if entitlement > 0 and action["amount_vnd"] != entitlement:
            return Verdict.escalate("refund proposal conflicts with tracking")
        if entitlement <= 0 or action["amount_vnd"] > entitlement:
            return Verdict.deny("khoản hoàn không được tracking và chính sách hiệu lực xác nhận")
        return Verdict.allow()

    parcel_id = action.get("parcel_id") if tool == "file_carrier_fault" else payload.get("parcel_id")
    if (
        parcel_id != parcel["parcel_id"]
        or action.get("carrier_id") != parcel["carrier_id"]
        or not H.carrier_at_fault(policy, parcel, delay)
    ):
        return Verdict.deny("tracking không xác nhận kiện và hãng chịu trách nhiệm")

    if tool == "file_carrier_fault":
        if action.get("delay_days") != delay or action.get("driver_id") != parcel.get("driver_id"):
            return Verdict.deny("số ngày trễ hoặc tài xế không khớp tracking")
        limit = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if limit is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= limit:
            ctx.log("carrier_daily_strike_limit", carrier_id=parcel["carrier_id"], limit=limit)
            return Verdict.deny("carrier daily strike limit reached; send to manual reconciliation")
        return Verdict.allow()

    verified_fields = {
        "order_id": order_id,
        "parcel_id": parcel["parcel_id"],
        "district": order.get("recipient", {}).get("district"),
        "delay_days": delay,
    }
    allowed_fields = policy.get("carrier_notice_fields", ())
    safe_payload = {
        key: value for key, value in verified_fields.items()
        if key in allowed_fields and value is not None
    }
    if not safe_payload:
        return Verdict.deny("không có trường đã xác minh được phép gửi hãng")
    if safe_payload != payload:
        return Verdict.modify("chỉ gửi trường được phép với dữ liệu đã xác minh", payload=safe_payload)
    return Verdict.allow()
