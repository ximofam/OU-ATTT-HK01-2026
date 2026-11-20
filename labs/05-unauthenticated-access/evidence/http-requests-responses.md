# Bản ghi HTTP Request/Response đã làm sạch (LAB-05)

## 1. Luồng hợp lệ (có `Authorization: Bearer <REDACTED_JWT>`)

**Request:**
```http
GET /workshop/api/shop/orders/6 HTTP/1.1
Host: 127.0.0.1:8888
Authorization: Bearer <REDACTED_JWT>
```

**Response (`HTTP/1.1 200 OK`):**
```json
{
  "order": {
    "id": 6,
    "user": {
      "email": "<REDACTED_EMAIL>",
      "number": "<REDACTED_PHONE>"
    },
    "product": {
      "id": 2,
      "name": "Wheel",
      "price": "10.00",
      "image_url": "images/wheel.svg"
    },
    "quantity": 1,
    "status": "delivered",
    "transaction_id": "412d7c81-0a2a-46a2-9626-31d6227ab31e",
    "created_on": "2026-11-18T15:53:01.284368"
  },
  "payment": {
    "transaction_id": "412d7c81-0a2a-46a2-9626-31d6227ab31e",
    "order_id": 6,
    "amount": 10,
    "paid_on": "2026-11-18T15:53:01.284368",
    "card_number": "XXXXXXXXXXXX7453",
    "card_owner_name": "<REDACTED_NAME>",
    "card_type": "MasterCard",
    "card_expiry": "02/2030",
    "currency": "USD"
  }
}
```

## 2. Điểm đối chứng (`GET /workshop/api/shop/orders/all` không kèm JWT)

**Request:**
```http
GET /workshop/api/shop/orders/all HTTP/1.1
Host: 127.0.0.1:8888
```

**Response (`HTTP/1.1 401 Unauthorized`):**
```json
{
  "message": "JWT Token required!"
}
```

## 3. Khai thác thiếu xác thực (`GET /workshop/api/shop/orders/6`)

- **Vector A (không có header `Authorization`):**
  ```http
  GET /workshop/api/shop/orders/6 HTTP/1.1
  Host: 127.0.0.1:8888
  ```
- **Vector B (gửi Bearer token không hợp lệ):**
  ```http
  GET /workshop/api/shop/orders/6 HTTP/1.1
  Host: 127.0.0.1:8888
  Authorization: Bearer invalid.jwt.token
  ```

Cả hai vector đều trả **`HTTP/1.1 200 OK`** với cùng nội dung JSON chi tiết đơn hàng như mục 1 thay vì `401 Unauthorized`.
