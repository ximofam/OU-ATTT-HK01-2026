# ROADMAP 7 ngày — Nhóm 5 thành viên

**Quy tắc:** Mỗi người làm 1 Lab và 1 file test. Các hoạt động cuối ngày được báo cáo ngắn gọn, blocker > 2 giờ phải thông báo cả nhóm.

| Ngày | Công việc của mọi thành viên | Điều kiện hoàn thành |
|---|---|---|
| **D1 — Setup** | Cài Docker/crAPI, Python; clone repo; chọn Lab | crAPI chạy được, mỗi người có branch riêng |
| **D2 — Recon** | Khảo sát endpoint, workflow, account, xây dựng giả thuyết lỗi | Mỗi người có kịch bản thử nghiệm nháp |
| **D3 — Manual testing** | Thực hiện kiểm thử trong Lab, xác minh lỗi | Có bằng chứng kỹ thuật bước đầu |
| **D4 — Freeze Lab** | Hoàn thiện demo, lưu request/response, ghi điều kiện tái hiện | 5 Lab đạt hoặc blocker rõ ràng; ngừng mở rộng phạm vi |
| **D5 — Automation** | Viết Python security tests, phân tích root cause và mitigation | Test chạy thật và có kết luận trung thực (PASS/FAIL) |
| **D6 — Reporting** | Hoàn thiện case study, review chéo, tổng hợp report/slide | Báo cáo và slide v1, có fallback demo |
| **D7 — Rehearsal** | Tổng duyệt, xử lý blocker nhỏ, chuẩn bị nộp | Demo từ môi trường sạch, kết quả khớp báo cáo |

## Quality Gates

### Cuối ngày 1

- [ ] Có ít nhất một máy chạy crAPI ổn định, tốt nhất cả nhóm có môi trường local.
- [ ] Có thể truy cập `http://127.0.0.1:8888`.
- [ ] Biết phiên bản/commit crAPI và cách chạy lại môi trường.
- [ ] Mỗi thành viên có branch riêng, scope riêng, biết cách mở PR.

### Cuối ngày 4

- [ ] Mỗi Lab có request/response minh họa và mô tả kết quả.
- [ ] Đã xác định chính xác điều kiện cần để tái hiện, dùng tài khoản/dữ liệu giả.
- [ ] Chốt 5 challenge, không thêm lỗi mới khi chưa hoàn thiện.

### Cuối ngày 6

- [ ] Mọi thành viên có báo cáo riêng theo cùng mẫu.
- [ ] Các test không còn ở trạng thái TODO/SKIPPED nếu được tuyên bố hoàn thành.
- [ ] Kết quả test không bị diễn giải sai: FAIL trên vulnerable target có thể là kết quả dự kiến.
- [ ] Slide, báo cáo tổng và ảnh/video demo dự phòng sẵn sàng.

## Nếu thiếu thời gian

1. Giữ 5 Lab chính và bằng chứng tái hiện.
2. Hoàn thiện ít nhất 1 test bảo mật cho mỗi Lab.
3. Đề xuất mitigation trong báo cáo.
4. Chỉ làm bản vá chạy được, GitHub Actions hoặc Dashboard nếu các mục trên đã xong.
