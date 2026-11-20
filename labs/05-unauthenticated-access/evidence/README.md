# Bằng chứng LAB-05 — Unauthenticated Access

Tất cả hình ảnh và request/response đã được làm sạch: JWT, email và số điện thoại tài khoản thử được che hoặc thay bằng placeholder trước khi đưa lên repo.

- `01-shop-order-details-ui.png` — Giao diện Web xem chi tiết đơn hàng hợp lệ khi đã đăng nhập (đã che PII).
- `02-curl-unauthenticated-access.png` — Kiểm chứng bằng `curl`: đối chứng `/orders/all` trả `401` so với `/orders/6` trả `200 OK` không cần token.
- `03-pytest-security-result.png` — Kết quả chạy `pytest tests/security/test_unauthenticated_access.py -v --tb=short`.
- `http-requests-responses.md` — Bản ghi HTTP request/response đã làm sạch cho luồng hợp lệ, đối chứng `401` và truy cập không xác thực `200 OK`.
