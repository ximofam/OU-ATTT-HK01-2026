# Bằng chứng LAB-05 — Unauthenticated Access

Tất cả request/response phải được làm sạch: JWT, email và số điện thoại tài khoản thử được
thay bằng placeholder trước khi đưa lên repo.

- `01-normal-flow.md` — luồng đăng ký, đăng nhập, tạo đơn và xem chi tiết đơn hàng hợp lệ.
- `02-control-orders-all-401.md` — đối chứng `GET /workshop/api/shop/orders/all` không có
  token trả về `401 Unauthorized`.
- `03-unauthenticated-order-detail.md` — truy cập `GET /workshop/api/shop/orders/{order_id}`
  không có token / sai token vẫn trả về `200 OK` kèm dữ liệu đơn hàng và PII.
- `pytest-vulnerable-run.txt` — output thật của security test trên crAPI local chưa vá.
