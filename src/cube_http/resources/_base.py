import httpx

__all__ = ["SyncApiResource", "AsyncApiResource"]


class SyncApiResource:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client


class AsyncApiResource:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
