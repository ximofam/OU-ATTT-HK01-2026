# Bằng chứng LAB-04 — Mass Assignment

Tất cả request/response đã được làm sạch: JWT, email và số điện thoại tài khoản thử đã
được thay bằng placeholder.

- [01-normal-flow.md](01-normal-flow.md) — luồng mua hàng và hoàn hàng hợp lệ.
- [02-negative-quantity.md](02-negative-quantity.md) — tăng credit bằng `quantity` âm.
- [03-mass-assignment-put.md](03-mass-assignment-put.md) — sửa `quantity`/`status` qua
  shadow API `PUT /workshop/api/shop/orders/{order_id}`.
- [pytest-vulnerable-run.txt](pytest-vulnerable-run.txt) — output thật của security test
  trên crAPI chưa vá.
