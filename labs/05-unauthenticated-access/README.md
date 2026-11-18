# LAB-05 — Unauthenticated Access

**Challenge chính thức:** #14 — Find an endpoint missing authentication checks.  
**Thư mục test:** `tests/security/test_unauthenticated_access.py`

## Cần thực hiện

- [x] Nghiên cứu cơ chế xác thực API và khác biệt giữa 401/403.
- [x] Khảo sát chức năng hợp lệ cần phải đăng nhập.
- [ ] Kiểm tra request khi có và không có thông tin xác thực trong local crAPI.
- [ ] Tái hiện challenge và thu thập bằng chứng.
- [x] Phân tích nguyên nhân thiếu middleware/kiểm tra xác thực.
- [x] Viết test Python xác minh endpoint được bảo vệ từ chối request không có token.
- [x] Đề xuất kiểm tra authentication tập trung và test case kiểm chứng.
- [ ] Hoàn thiện báo cáo và demo.

## Đầu ra

- Hoàn thiện `REPORT.md`.
- Bằng chứng trong `evidence/`.
- File test chạy được và kết quả thật.
