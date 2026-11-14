"""LAB-02: BFLA — invoking a privileged video operation."""

import pytest


@pytest.mark.security
@pytest.mark.skip(reason="TODO TV2: implement verified local crAPI BFLA test")
def test_regular_user_cannot_invoke_admin_video_delete(api_client):
    """Prepare throwaway video data and a low-privilege account.

    Do not delete any data outside your own isolated local Lab.
    """
    raise NotImplementedError
