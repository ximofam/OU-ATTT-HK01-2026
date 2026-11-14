"""LAB-05: Unauthenticated Access — missing login checks."""

import pytest


@pytest.mark.security
@pytest.mark.skip(reason="TODO TV5: implement verified local unauthenticated access test")
def test_protected_endpoint_rejects_requests_without_token(api_client):
    """Identify an endpoint requiring auth, then call it without credentials."""
    raise NotImplementedError
