"""LAB-03: Excessive Data Exposure — sensitive information in API responses."""

import pytest


@pytest.mark.security
@pytest.mark.skip(reason="TODO TV3: implement verified local data exposure test")
def test_api_does_not_expose_other_users_sensitive_fields(api_client):
    """Identify a relevant endpoint and define an explicit safe response schema."""
    raise NotImplementedError
