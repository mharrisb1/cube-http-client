import pytest


@pytest.fixture()
def url() -> str:
    return "http://localhost:4000/cubejs-api"


@pytest.fixture()
def token() -> str:
    return "i9f5e76b519a44b060daa33e78c5de170"
