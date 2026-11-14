"""LAB-04: Mass Assignment — unauthorized refund/order property changes."""

import pytest


@pytest.mark.security
@pytest.mark.skip(reason="TODO TV4: implement verified local mass assignment test")
def test_client_cannot_override_protected_refund_fields(api_client):
    """Create a throwaway order, then verify protected fields are server-owned."""
    raise NotImplementedError
