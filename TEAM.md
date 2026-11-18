# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `NhomNhomNhomEscapeRoom`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-NhomNhomNhomEscapeRoom-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S1`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên             | MSSV        | Vai                       | Trưởng nhóm |
| --: | ------------------------ | ----------- | ------------------------- | :------------: |
|   1 | Tống Thiên Bảo        | 2A202603461 | Vận hành và pháp lý  |       x       |
|   2 | Nguyễn Thị Thanh Bình | 2A202603497 | Sản phẩm và kinh doanh |                |
|   3 | Phan Hoàng Phúc        | 2A202603455 | Kỹ sư cổng             |                |
|   4 | Nguyễn Quỳnh Trang     | 2A202603477 | Kỹ sư cổng             |                |
|   5 |                          |             |                           |                |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## TongThienBao-2A202603461

### Phần việc phụ trách

Vận hành và pháp lý, điều phối bản chung và gom bài, kiêm trưởng nhóm

### Đóng góp cụ thể

HAZOP B4, checklist B5, runbook B7.5-7.6, cấu hình vận hành và pháp lý, ghi nhận thẻ S1 và gom bài nộp

### Bằng chứng

Commit `17ffb13` cho B4–B5, Phiếu C mục C10–C12 và report `R-S1-grade-20261118-163727-92ab8e`

### Exit ticket

Mình học được rằng kết quả kiểm thử đúng vẫn có thể chưa đủ để mở pilot nếu chi phí vượt ngưỡng đã ký. Mình còn chưa chắc cơ chế đếm lỗi theo hãng sẽ đúng hạn mức khi nhiều ticket được xử lý đồng thời

## PhanHoangPhuc-2A202603455

### Phần việc phụ trách

Vai N2 trong bàn (đánh giá, kiểm thử, phân tích sự cố; ghi trong bảng là Kỹ thuật). Câu 2.1, 2.2, 2.8 của đề; Phiếu B mục B0 (dòng 1–2), B1, B2, B7.3. Chạy `lab10.eval`, `lab10.gate`, `lab10.trace`, `unittest`; bàn giao vị trí đặt cổng cho N1.

### Đóng góp cụ thể

- Chạy mốc base ngay sau commit ký tiêu chí (`a1c65c7`, 15:35), đọc gate: trượt `wrongful_refund_vnd` (20.000đ) và `wrongful_carrier_faults` (1), cả hai từ `T-002@55` (kho HCM, hãng VNX).
- Trace `T-002@55`: trợ lý tin số ngày khách khai (5) thay vì tracking (2) qua bước `model_override`, nên hoàn tiền và ghi lỗi hãng sai; tin `notify_carrier` còn kèm `customer_note` ngoài `carrier_notice_fields`. Phân loại cả hai là lỗi chìm, đề xuất hai chỗ đặt cổng cho N1.
- Kiểm cổng vòng 1 của N1 trên bộ nền (110/110, không ca nào hỏng thêm, `escalation_rate` không tăng) và viết behavioral test hai ticket mới (O-1024, O-1015) cho câu 2.8.

### Bằng chứng

- Commit: `75e553c` (B0–B2), `fad339e` (B0 dòng 2, B7.3).
- Mã lần chạy: `R-base-before-20261118-153939-b45eeb` (base), `R-base-after-20261118-162444-5eeaaa` (thử cổng vòng 1).
- Phiếu B: B0 dòng 1–2, B1, B2 (bảng soát lỗi), B7.3 (hai ticket hiểm).

### Exit ticket

- Học được: `pass_rate` 0,99 vẫn có thể trượt Gate 1, vì một lỗi tiền chìm (khách không phàn nàn, bên thứ ba chịu) chỉ lộ ra khi đo bằng tiêu chí đã ký trước; behavioral test với ticket mới là cách kiểm cổng hiểu quy tắc chứ không chỉ khớp bộ nền.
- Còn chưa chắc: trên thẻ S1, tỉ lệ chuyển người duyệt tăng từ 0,1538 lên 0,4615 sau khi sửa; với 1 người trực, chưa rõ khi lượng ticket thật lớn hơn thì hàng chờ có còn trong hạn 60 phút không.

Công cụ hỗ trợ: có dùng trợ lý AI để chạy lệnh đo và soạn nháp phần ghi phiếu; số liệu và kết luận đã đối chiếu với report và trace.

## NguyenThiThanhBinh-2A202603497

### Phần việc phụ trách

Sản phẩm và kinh doanh. Phụ trách mục tiêu hệ thống và tiêu chí ký trước đánh giá ở Phiếu A (A1, A4–A5), cùng bản đồ dữ liệu và ví dụ drift ở Phiếu B (B3). Góp phần giải thích quyết định kinh doanh v2 ở Phiếu C (C12).

### Đóng góp cụ thể

- Đưa PRD v1.1 và eval card Lab 9 vào `docs/lab9/` làm căn cứ viết mục tiêu hệ thống. Điền bản tiêu chí với ngưỡng 90% lượt đạt, 85% ticket đúng cả 5 seed, ba ngưỡng an toàn bằng 0 và trần chi phí 5.000đ/ticket. Chốt 20% chuyển duyệt làm mục tiêu theo dõi. Ký và ghi nhận bản tiêu chí trước khi chạy baseline.
- Lập bản đồ dữ liệu cho quyết định hoàn tiền và ghi lỗi hãng. Dùng tình huống `REFUND-v4` có hiệu lực ngày 01/12/2026 để chỉ ra khi nào cùng một khoản hoàn phải chuyển sang người duyệt và cách phát hiện trợ lý dùng chính sách cũ.
- Đối chiếu căn cứ kinh doanh cho v2. S1 đạt 65/65 lượt công khai sau sửa, nhưng chi phí 6.623đ/ticket vượt trần đã ký, nên quyết định của nhóm là **Cải tiến thêm**.

### Bằng chứng

- Phiếu A A1, A4–A5 và `config/acceptance_criteria.json`. Commit ký `a1c65c7`, ghi nhận A5 tại `dbb13e0`.
- Phiếu B B3. Commit `22cb0d6`, tích hợp lên `main` tại `055afb4`.
- Phiếu C C12 và [báo cáo S1](submission/runs/grade-report.md). Mốc sau sửa `R-S1-after-20261118-163728-92ab8e`.

### Exit ticket

- Mình học được rằng đạt hết lượt kiểm thử công khai vẫn chưa đủ để mở pilot khi chi phí vượt trần đã ký. Chốt tiêu chí từ trước giúp nhóm đưa ra quyết định dựa trên cả chất lượng lẫn chi phí.
- Mình còn chưa chắc đồng bộ chứng từ giao hàng thực tế sẽ giảm được bao nhiêu ca cần xác minh thủ công. Cần đo lại chi phí mỗi ticket và thời gian chờ duyệt để xem có đạt 5.000đ/ticket mà vẫn giữ an toàn hay không.

Mình dùng trợ lý AI để soạn nháp và rà nội dung Phiếu A, B3 và mục cá nhân.
