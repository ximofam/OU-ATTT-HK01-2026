"""LAB-04 / TC-01: client must not force an order into the returned state.

Run live only against your own local crAPI with CRAPI_LAB04_RUN=1. The test
creates and pays for one new fake order; it does not restore the account.
"""

import json
import os
from decimal import Decimal, InvalidOperation

import httpx
import pytest


def _setup_error(message: str) -> None:
    pytest.fail(f"SETUP_ERROR: {message}", pytrace=False)


def _request(client: httpx.Client, method: str, path: str, **kwargs) -> httpx.Response:
    try:
        return client.request(method, path, **kwargs)
    except httpx.RequestError:
        _setup_error(f"cannot reach local crAPI for {method} {path}; check Docker/base URL")


def _object(response: httpx.Response, step: str) -> dict:
    try:
        data = response.json()
    except ValueError:
        _setup_error(f"{step}: response was not JSON")
    if not isinstance(data, dict):
        _setup_error(f"{step}: expected a JSON object")
    return data


def _money(value: object, step: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        _setup_error(f"{step}: credit/price is not a valid number")
    if not amount.is_finite():
        _setup_error(f"{step}: credit/price must be finite")
    return amount


def _catalog(client: httpx.Client, headers: dict) -> tuple[list, Decimal]:
    response = _request(
        client, "GET", "/workshop/api/shop/products",
        headers=headers, params={"limit": 30, "offset": 0},
    )
    if response.status_code != 200:
        _setup_error(f"GET products: HTTP {response.status_code}; check login/API version")
    data = _object(response, "GET products")
    if not isinstance(data.get("products"), list) or "credit" not in data:
        _setup_error("GET products: missing products/credit fields")
    return data["products"], _money(data["credit"], "GET products credit")


def _order(client: httpx.Client, headers: dict, order_id: int) -> dict:
    response = _request(
        client, "GET", "/workshop/api/shop/orders/all",
        headers=headers, params={"limit": 30, "offset": 0},
    )
    if response.status_code != 200:
        _setup_error(f"GET orders/all: HTTP {response.status_code}")
    orders = _object(response, "GET orders/all").get("orders")
    if not isinstance(orders, list):
        _setup_error("GET orders/all: missing orders list")
    match = next(
        (item for item in orders if isinstance(item, dict) and item.get("id") == order_id),
        None,
    )
    if match is None or not isinstance(match.get("status"), str):
        _setup_error(f"GET orders/all: newly created order {order_id} not found/invalid")
    return match


def _assert_server_owned(
    status_before: str,
    status_after: str,
    credit_before: Decimal,
    credit_after: Decimal,
) -> None:
    """The client must not change an order's return state or trigger a refund."""
    assert status_after == status_before and credit_after <= credit_before, (
        "SECURITY_VIOLATION: client-controlled status/refund changed server-owned "
        f"data: status {status_before!r} -> {status_after!r}; "
        f"credit {credit_before} -> {credit_after}"
    )
    if credit_after < credit_before:
        pytest.fail(
            "SETUP_ERROR: credit decreased during the isolated order test; "
            "check for concurrent account activity",
            pytrace=False,
        )


@pytest.mark.security
@pytest.mark.skipif(
    os.environ.get("CRAPI_LAB04_RUN") != "1",
    reason="Live TC-01 requires CRAPI_LAB04_RUN=1 (creates a paid order)",
)
def test_client_cannot_override_protected_refund_fields(api_client):
    """TC-01: reject PUT status=returned on a newly purchased dummy order.

    On vulnerable crAPI this is expected to FAIL with SECURITY_VIOLATION.
    """
    if os.environ.get("CRAPI_LAB04_RUN") != "1":
        pytest.skip("Live TC-01 requires CRAPI_LAB04_RUN=1 (creates a paid order)")

    email = os.environ.get("CRAPI_USER_A_EMAIL")
    password = os.environ.get("CRAPI_USER_A_PASSWORD")
    if not email or not password:
        _setup_error("set CRAPI_USER_A_EMAIL and CRAPI_USER_A_PASSWORD for a dummy account")

    login = _request(
        api_client, "POST", "/identity/api/auth/login",
        json={"email": email, "password": password},
    )
    if login.status_code != 200:
        _setup_error(f"login HTTP {login.status_code}; check dummy account credentials")
    token = _object(login, "POST login").get("token")
    if not isinstance(token, str) or not token:
        _setup_error("login: response has no token")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        product_id = int(os.environ.get("CRAPI_LAB04_PRODUCT_ID", "2"))
    except ValueError:
        _setup_error("CRAPI_LAB04_PRODUCT_ID must be an integer (default: 2 / Wheel)")
    products, available_credit = _catalog(api_client, headers)
    product = next(
        (item for item in products if isinstance(item, dict) and item.get("id") == product_id),
        None,
    )
    if product is None or "price" not in product:
        _setup_error(f"product_id={product_id} not found in first 30 shop products")
    unit_price = _money(product["price"], "selected product price")
    if unit_price <= 0 or available_credit < unit_price:
        _setup_error("selected product must cost > 0 and be affordable with dummy credit")

    purchase = _request(
        api_client, "POST", "/workshop/api/shop/orders",
        headers=headers, json={"product_id": product_id, "quantity": 1},
    )
    if purchase.status_code not in {200, 201}:
        _setup_error(f"create throwaway order: HTTP {purchase.status_code}")
    order_id = _object(purchase, "POST orders").get("id")
    if type(order_id) is not int or order_id <= 0:
        _setup_error("POST orders: no positive integer order id")

    order_before = _order(api_client, headers, order_id)
    status_before = order_before["status"]
    if status_before != "delivered" or order_before.get("quantity") != 1:
        _setup_error("new order is not delivered with quantity=1; cannot run TC-01")
    _, credit_before = _catalog(api_client, headers)  # After paying, before the attack.

    attack = _request(
        api_client, "PUT", f"/workshop/api/shop/orders/{order_id}",
        headers=headers, json={"status": "returned"},
    )
    if attack.status_code not in {200, 201, 204, 400, 403, 422}:
        _setup_error(f"PUT order: unexpected HTTP {attack.status_code}; check API version")

    # Verify via two independent GETs; never infer success from PUT's response.
    status_after = _order(api_client, headers, order_id)["status"]
    _, credit_after = _catalog(api_client, headers)
    print(
        f"TC-01 order={order_id}, PUT HTTP={attack.status_code}; "
        f"status: {status_before} -> {status_after}; "
        f"credit: {credit_before} -> {credit_after}"
    )
    _assert_server_owned(status_before, status_after, credit_before, credit_after)


def test_tc01_invariant_accepts_an_unchanged_order_and_credit():
    """A rejected status override must preserve both server-owned fields."""
    _assert_server_owned("delivered", "delivered", Decimal("90"), Decimal("90"))


def test_tc01_invariant_detects_an_unauthorized_return():
    """A forced returned status is a finding even if no credit is added."""
    with pytest.raises(AssertionError, match="SECURITY_VIOLATION"):
        _assert_server_owned("delivered", "returned", Decimal("90"), Decimal("90"))


def test_tc01_invariant_detects_an_unauthorized_credit_increase():
    """An unexpected credit increase is a finding even if status is unchanged."""
    with pytest.raises(AssertionError, match="SECURITY_VIOLATION"):
        _assert_server_owned("delivered", "delivered", Decimal("90"), Decimal("100"))


def test_tc01_requires_explicit_opt_in_without_any_network_request(monkeypatch):
    """Running the default suite must never purchase a shop order."""
    monkeypatch.delenv("CRAPI_LAB04_RUN", raising=False)

    def fail_if_called(_request):
        raise AssertionError("Live TC-01 made an unexpected HTTP request")

    with httpx.Client(transport=httpx.MockTransport(fail_if_called)) as client:
        with pytest.raises(pytest.skip.Exception, match="CRAPI_LAB04_RUN=1"):
            test_client_cannot_override_protected_refund_fields(client)


@pytest.mark.parametrize("vulnerable", [False, True], ids=["protected", "vulnerable"])
def test_tc01_offline_flow_detects_unauthorized_return(monkeypatch, vulnerable):
    """The live TC-01 flow must distinguish rejected and exploited returns."""
    monkeypatch.setenv("CRAPI_LAB04_RUN", "1")
    monkeypatch.setenv("CRAPI_USER_A_EMAIL", "user@example.invalid")
    monkeypatch.setenv("CRAPI_USER_A_PASSWORD", "dummy-only")
    state = {"credit": Decimal("100"), "order": None}
    requests = []

    def local_shop(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        requests.append((request.method, path))
        if path == "/identity/api/auth/login" and request.method == "POST":
            assert json.loads(request.content) == {
                "email": "user@example.invalid", "password": "dummy-only"
            }
            return httpx.Response(200, json={"token": "fake-jwt"})

        assert request.headers.get("Authorization") == "Bearer fake-jwt"
        if path == "/workshop/api/shop/products" and request.method == "GET":
            return httpx.Response(200, json={
                "products": [{"id": 2, "name": "Wheel", "price": "10.00"}],
                "credit": float(state["credit"]),
            })

        if path == "/workshop/api/shop/orders" and request.method == "POST":
            assert json.loads(request.content) == {"product_id": 2, "quantity": 1}
            state["order"] = {"id": 501, "status": "delivered", "quantity": 1}
            state["credit"] -= Decimal("10")
            return httpx.Response(200, json={"id": 501, "credit": 90})

        if path == "/workshop/api/shop/orders/all" and request.method == "GET":
            return httpx.Response(200, json={"orders": [state["order"]]})

        if path == "/workshop/api/shop/orders/501" and request.method == "PUT":
            assert json.loads(request.content) == {"status": "returned"}
            if not vulnerable:
                return httpx.Response(403, json={"message": "Forbidden"})
            state["order"]["status"] = "returned"
            state["credit"] += Decimal("10")
            return httpx.Response(200, json={"orders": state["order"]})

        raise AssertionError(f"Unexpected TC-01 request: {request.method} {path}")

    with httpx.Client(
        base_url="http://127.0.0.1:8888",
        transport=httpx.MockTransport(local_shop),
    ) as client:
        if vulnerable:
            with pytest.raises(AssertionError, match="SECURITY_VIOLATION"):
                test_client_cannot_override_protected_refund_fields(client)
        else:
            test_client_cannot_override_protected_refund_fields(client)

    assert requests.count(("GET", "/workshop/api/shop/orders/all")) == 2
    assert ("PUT", "/workshop/api/shop/orders/501") in requests
