"""LAB-05: Unauthenticated Access — missing authentication checks (Challenge #14)."""

import uuid

import pytest


PASSWORD = "Lab05@12345"


def _signup_and_login(api_client):
    """Create a throwaway test account in local crAPI and return an Authorization header."""
    email = f"lab05-{uuid.uuid4().hex[:12]}@example.com"
    number = f"09{uuid.uuid4().int % 10**9:09d}"
    signup = api_client.post(
        "/identity/api/auth/signup",
        json={
            "name": "Lab05 User",
            "email": email,
            "number": number,
            "password": PASSWORD,
        },
    )
    assert signup.status_code == 200, f"signup failed: {signup.status_code} {signup.text}"

    login = api_client.post(
        "/identity/api/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert login.status_code == 200, f"login failed: {login.status_code} {login.text}"
    return {"Authorization": f"Bearer {login.json()['token']}"}


def _create_seed_order(api_client, headers):
    """Create one valid shop order using the authenticated test account and return order_id."""
    products_resp = api_client.get(
        "/workshop/api/shop/products?offset=0&limit=10",
        headers=headers,
    )
    assert products_resp.status_code == 200, products_resp.text
    products = products_resp.json()["products"]
    assert len(products) > 0, "shop has no seeded products"

    created = api_client.post(
        "/workshop/api/shop/orders",
        headers=headers,
        json={"product_id": products[0]["id"], "quantity": 1},
    )
    assert created.status_code == 200, created.text
    return created.json()["id"]


@pytest.mark.security
def test_orders_list_rejects_requests_without_token(api_client):
    """Control check: GET /workshop/api/shop/orders/all properly enforces @jwt_auth_required."""
    headers = _signup_and_login(api_client)

    auth_resp = api_client.get("/workshop/api/shop/orders/all", headers=headers)
    assert auth_resp.status_code == 200, auth_resp.text

    unauth_resp = api_client.get("/workshop/api/shop/orders/all")
    assert unauth_resp.status_code == 401, (
        "expected control endpoint /workshop/api/shop/orders/all to return 401 without JWT, "
        f"got HTTP {unauth_resp.status_code}"
    )


@pytest.mark.security
def test_protected_endpoint_rejects_requests_without_token(api_client):
    """Verify GET /workshop/api/shop/orders/{id} rejects requests without Authorization header."""
    headers = _signup_and_login(api_client)
    order_id = _create_seed_order(api_client, headers)
    target_path = f"/workshop/api/shop/orders/{order_id}"

    # 1. Valid authenticated request succeeds
    auth_resp = api_client.get(target_path, headers=headers)
    assert auth_resp.status_code == 200, auth_resp.text

    # 2. Unauthenticated request (no Authorization header, clean cookies) must return 401
    api_client.cookies.clear()
    unauth_resp = api_client.get(target_path)

    exposed_keys = []
    if unauth_resp.status_code == 200:
        order_data = unauth_resp.json().get("order", {})
        exposed_keys = sorted(order_data.keys())

    assert unauth_resp.status_code == 401, (
        f"unauthenticated access detected on GET {target_path}: expected HTTP 401 without token, "
        f"but got HTTP {unauth_resp.status_code} exposing order fields {exposed_keys}"
    )


@pytest.mark.security
def test_protected_endpoint_rejects_invalid_bearer_token(api_client):
    """Verify GET /workshop/api/shop/orders/{id} rejects malformed/invalid Bearer tokens."""
    headers = _signup_and_login(api_client)
    order_id = _create_seed_order(api_client, headers)
    target_path = f"/workshop/api/shop/orders/{order_id}"

    invalid_resp = api_client.get(
        target_path,
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )
    assert invalid_resp.status_code == 401, (
        f"authentication bypass detected on GET {target_path}: endpoint ignored invalid Bearer "
        f"token and returned HTTP {invalid_resp.status_code} (expected HTTP 401)"
    )
