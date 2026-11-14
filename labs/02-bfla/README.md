# LAB-02 — Broken Function Level Authorization (BFLA)

**Challenge chính thức:** #7 — Delete a video of another user.  
**Thư mục test:** `tests/security/test_bfla.py`

## Cần thực hiện

- [ ] Nghiên cứu BFLA và phân biệt với BOLA.
- [ ] Tạo tài khoản thử nghiệm và video giả chỉ phục vụ Lab.
- [ ] Khảo sát API video và chức năng dành cho các cấp quyền khác nhau.
- [ ] Thực nghiệm việc gọi chức năng vượt quyền trong local crAPI.
- [ ] Lưu bằng chứng request/response đã làm sạch.
- [ ] Phân tích quyền theo role/function ở Backend.
- [ ] Viết test Python xác minh tài khoản thường không gọi được chức năng đặc quyền.
- [ ] Viết mitigation và kịch bản kiểm thử lại.

## Đầu ra

- Hoàn thiện `REPORT.md` theo mẫu chung.
- Bằng chứng trong `evidence/`.
- File test có thể thực thi và kết quả thật.

**An toàn:** Chỉ thao tác trên video thử nghiệm do nhóm tự tạo.
