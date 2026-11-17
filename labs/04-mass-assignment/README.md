# LAB-04 — Mass Assignment

**Challenge chính thức:** #8 — Get an item for free through an invalid refund workflow.  
**Thư mục test:** `tests/security/test_mass_assignment.py`

## Cần thực hiện

- [x] Nghiên cứu Mass Assignment và rủi ro client có thể sửa thuộc tính nội bộ.
- [x] Tạo tài khoản/đơn hàng giả trong local crAPI.
- [x] Khảo sát workflow hoàn tiền hợp lệ và các request liên quan.
- [x] Kiểm thử cách API xử lý các thuộc tính không được phép thay đổi.
- [x] Ghi lại trước/sau bằng chứng, tránh thao tác dữ liệu ngoài Lab.
- [x] Phân tích vì sao Backend tin tưởng dữ liệu client không phù hợp.
- [x] Viết test Python xác minh các thuộc tính nhạy cảm do server quản lý.
- [x] Đề xuất allowlist fields, authorization và validation nghiệp vụ.

## Đầu ra

- Hoàn thiện `REPORT.md`.
- Bằng chứng trong `evidence/`.
- File test chạy được và kết quả thật.
