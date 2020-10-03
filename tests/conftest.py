import pytest

from webhooks import app


@pytest.fixture
def client():
    yield app.test_client()
