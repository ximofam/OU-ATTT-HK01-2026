# LAB-03 — Excessive Data Exposure

**Challenge chính thức:** #4 — API leaks sensitive information of other users.  
**Thư mục test:** `tests/security/test_data_exposure.py`

## Cần thực hiện

- [ ] Nghiên cứu nguyên tắc giới hạn dữ liệu trả về từ API.
- [ ] Khảo sát response schema và dữ liệu cần thiết cho chức năng hợp lệ.
- [ ] Tìm endpoint liên quan đến challenge chính thức trong local crAPI.
- [ ] Kiểm chứng dữ liệu thừa hoặc nhạy cảm bị đưa vào response.
- [ ] Ghi bằng chứng và che mọi thông tin phiên/tài khoản giả lập.
- [ ] Đề xuất DTO/response filtering và kiểm tra quyền với từng thuộc tính.
- [ ] Viết Python test so sánh response với chính sách dữ liệu an toàn.
- [ ] Hoàn thiện báo cáo và demo.

## Đầu ra

- Hoàn thiện `REPORT.md`.
- Bằng chứng trong `evidence/`.
- File test chạy được và kết quả thật.
