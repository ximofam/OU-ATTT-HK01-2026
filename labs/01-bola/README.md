# LAB-01 — Broken Object Level Authorization (BOLA)

**Challenge chính thức:** #1 — Access details of another user's vehicle.  
**Thư mục test:** `tests/security/test_bola.py`

## Cần thực hiện

- [ ] Đọc OWASP API1:2023 về BOLA.
- [ ] Tạo 2 tài khoản giả lập và dữ liệu phương tiện tách biệt.
- [ ] Khảo sát request/response của chức năng phương tiện.
- [ ] Thử nghiệm kiểm soát quyền đọc object giữa hai tài khoản trong local crAPI.
- [ ] Lưu bằng chứng kỹ thuật đã che token và thông tin cá nhân.
- [ ] Phân tích nguyên nhân ở server-side authorization.
- [ ] Viết test Python kiểm tra người dùng không được đọc object của người khác.
- [ ] Ghi kết quả, mitigation và điều kiện để demo lại.

## Đầu ra

- Hoàn thiện `REPORT.md` theo mẫu chung.
- Bằng chứng trong `evidence/`.
- File test có thể thực thi (không còn SKIPPED) và kết quả thật.

**Tham khảo:** [OWASP BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/).
