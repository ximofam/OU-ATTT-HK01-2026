"""LAB-04: Mass Assignment — unauthorized refund/order property changes."""

import uuid

import pytest


PASSWORD = "Vien@12345"


def _signup_and_login(api_client):
    """Create a throwaway account and return an Authorization header."""
    email = f"vien-lab04-{uuid.uuid4().hex[:12]}@example.com"
    number = f"09{uuid.uuid4().int % 10**9:09d}"
    signup = api_client.post(
        "/identity/api/auth/signup",
        json={
            "name": "Vien Lab04",
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


def _shop_state(api_client, headers):
    """Return the current credit and product catalog for the logged-in user."""
    response = api_client.get(
        "/workshop/api/shop/products?offset=0&limit=10", headers=headers
    )
    assert response.status_code == 200, response.text
    body = response.json()
    return body["credit"], body["products"]


@pytest.mark.security
def test_order_rejects_non_positive_quantity(api_client):
    """A client must not gain credit by ordering a negative quantity."""
    headers = _signup_and_login(api_client)
    credit_before, products = _shop_state(api_client, headers)
    product = products[0]

    response = api_client.post(
        "/workshop/api/shop/orders",
        headers=headers,
        json={"product_id": product["id"], "quantity": -5},
    )
    credit_after, _ = _shop_state(api_client, headers)

    assert response.status_code == 400, (
        "crAPI accepted a negative order quantity instead of rejecting it: "
        f"HTTP {response.status_code}, credit {credit_before} -> {credit_after}, "
        f"body={response.text}"
    )
    assert credit_after == credit_before, (
        f"credit changed after an invalid order: {credit_before} -> {credit_after}"
    )


@pytest.mark.security
def test_client_cannot_override_protected_refund_fields(api_client):
    """Create a throwaway order, then verify protected fields are server-owned."""
    headers = _signup_and_login(api_client)
    _, products = _shop_state(api_client, headers)
    product = products[0]

    created = api_client.post(
        "/workshop/api/shop/orders",
        headers=headers,
        json={"product_id": product["id"], "quantity": 1},
    )
    assert created.status_code == 200, created.text
    order_id = created.json()["id"]
    credit_before, _ = _shop_state(api_client, headers)

    response = api_client.put(
        f"/workshop/api/shop/orders/{order_id}",
        headers=headers,
        json={"product_id": product["id"], "quantity": 100, "status": "returned"},
    )
    credit_after, _ = _shop_state(api_client, headers)

    assert response.status_code in {400, 403}, (
        "client was allowed to update server-owned order fields (quantity/status): "
        f"HTTP {response.status_code}, credit {credit_before} -> {credit_after}, "
        f"body={response.text}"
    )
    order = api_client.get(f"/workshop/api/shop/orders/{order_id}", headers=headers)
    assert order.json()["orders"]["quantity"] == 1
    assert credit_after == credit_before
