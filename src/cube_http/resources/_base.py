import httpx

__all__ = ["SyncApiResources", "AsyncApiResources"]


class SyncApiResources:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client


class AsyncApiResources:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
