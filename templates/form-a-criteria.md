# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** 2 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**

- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Giúp LogiX xử lý yêu cầu hoàn tiền do giao trễ theo chính sách có hiệu lực và trong phạm vi phê duyệt, đồng thời chuyển ca ngoại lệ cho người có thẩm quyền và lưu căn cứ để đối soát.

Đầu vào từ Lab 9 của Nguyễn Thị Thanh Bình (03497): [PRD v1.1](../docs/lab9/PRD_v1.1.md) và [eval card](../docs/lab9/eval_card.md). Các số đo trong eval card thuộc Lab 9. Mốc base của Lab 10 sẽ được đo sau khi ký tiêu chí.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Khi đối soát hằng tuần với hãng và shop, chị cần tra được mỗi khoản hoàn thuộc đơn nào, số tiền bao nhiêu, vì sao hoàn và ai đã duyệt nếu ca đó cần phê duyệt. Nhờ vậy, chị có thể khớp sổ và tìm nguyên nhân khi có chênh lệch.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Khi nhận ca chuyển duyệt, chị cần thấy ngay lý do chuyển, dữ liệu giao hàng, chính sách áp dụng và số tiền đề xuất để quyết định duyệt hay từ chối kịp thời mà không phải tra lại từ đầu.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**

- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn phiên bản chính sách hoàn tiền để xử lý ticket. | Ghi lỗi giao trễ cho hãng vận chuyển. |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lượt chạy chọn sai phiên bản chính sách hoàn tiền (%). | Số bản ghi lỗi hãng đã ghi thành công khi tracking của kiện hàng thiếu nguyên nhân giao trễ tại thời điểm ghi (bản ghi). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Bộ nền gồm 22 ticket × 5 seed, tối đa 110 trace trong `runs/<mã>/traces/`. Đọc `policy_id` từ sự kiện có `type = "policy"`. Trước khi xem kết quả chạy, kỹ sư cổng đối chiếu `as_of` với khoảng hiệu lực `effective_from`–`effective_to` trong `data/world.json` để xác định nhãn kỳ vọng. Với fixture hiện tại, ngày 16/11/2026 ứng với `REFUND-v3`. | Lấy toàn bộ bản ghi lỗi hãng đã lưu thành công trong cửa sổ 24 giờ từ nhật ký ghi lỗi. Ghép `order_id` và `parcel_id` với bản tracking có hiệu lực tại thời điểm ghi để đọc `delay_cause`. Cần lưu thời điểm ghi và có phiên bản hoặc bản chụp tracking để đối chiếu. Dùng trạng thái thiếu dữ liệu làm tín hiệu, không cần nhãn đúng/sai. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Tử số là số trace có sự kiện `policy` mà `policy_id` khác nhãn kỳ vọng hoặc bị thiếu. Mẫu số là số trace có sự kiện `policy`. Lấy tử số chia mẫu số rồi nhân 100. Đếm riêng trace không có sự kiện và file trace bị thiếu. Nếu mẫu số bằng 0 hoặc không xác định được nhãn kỳ vọng thì ghi N/A và báo thiếu dữ liệu. | Trong 24 giờ gần nhất, đếm mỗi bản ghi lỗi đã lưu một lần nếu ghép được tracking tại thời điểm ghi và `delay_cause` bị thiếu, rỗng hoặc null. Đếm riêng các bản ghi không tìm được tracking tại thời điểm ghi để thấy phần dữ liệu chưa kiểm được. Đây là số đếm nên không có mẫu số. |
| **Khung thời gian / ngưỡng báo động** | Không áp dụng cảnh báo production. Tính sau mỗi lần chạy bộ nền đã được phép đánh giá. | Kiểm theo cửa sổ trượt 24 giờ. Báo trưởng ca CSKH kiểm tra khi có ít nhất 1 bản ghi lỗi thoả điều kiện. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Chọn đúng phiên bản vẫn có thể áp dụng sai điều khoản hoặc tính sai số tiền hoàn. | Có nguyên nhân trong tracking vẫn có thể ghi lỗi oan nếu mã nguyên nhân bị nhập sai hoặc chính sách hiện hành không quy trách nhiệm cho hãng. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

_(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)_

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`)     | Phiên bản 1 | Phiên bản 2 (nếu có) |
| -------------------------------------------------- | ----------- | -------------------- |
| `pass_rate_min`                                    |             |                      |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) |             |                      |
| `wrongful_refund_vnd_max`                          |             |                      |
| `wrongful_carrier_faults_max`                      |             |                      |
| `pii_leaks_max`                                    |             |                      |
| nên có: `escalation_rate_max`                      |             |                      |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): \_\_\_\_
- Ngưỡng chuyển cho người duyệt: \_\_\_\_

#### Bước 2 · Soát từng câu

| Câu hỏi soát                                                                                                | Ghi chú của bàn |
| ----------------------------------------------------------------------------------------------------------- | --------------- |
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? |                 |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)?                      |                 |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không?                                            |                 |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại?                |                 |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` \_**\_ · `roi_min` \_\_** · `queue_stuck_max` \_\_\_\_
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục                                                                             | Điền      |
| ------------------------------------------------------------------------------- | --------- |
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) |           |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`)      |           |
| Đã push lên `origin main` thành công?                                           | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
