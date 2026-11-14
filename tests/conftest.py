"""Shared, deliberately small fixtures for authorized local crAPI testing."""

import os
from urllib.parse import urlparse

import httpx
import pytest
from dotenv import load_dotenv


load_dotenv()


@pytest.fixture(scope="session")
def crapi_base_url() -> str:
    url = os.environ.get("CRAPI_BASE_URL", "http://127.0.0.1:8888").rstrip("/")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "localhost",
        "127.0.0.1",
    }:
        raise ValueError("Security tests are restricted to local crAPI instances")
    return url


@pytest.fixture
def api_client(crapi_base_url: str):
    """Client for a crAPI instance started by the tester.

    Tests must explicitly create/fetch their own test data and authentication.
    """
    with httpx.Client(base_url=crapi_base_url, timeout=10.0) as client:
        yield client
