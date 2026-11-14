"""LAB-01: BOLA — access to another user's vehicle resource."""

import pytest


@pytest.mark.security
@pytest.mark.skip(reason="TODO TV1: implement verified local crAPI BOLA test")
def test_user_cannot_read_another_users_vehicle(api_client):
    """Set up A/B accounts; send user A's token for a vehicle belonging to B.

    Assert the expected authorization policy and document actual behavior.
    """
    raise NotImplementedError
