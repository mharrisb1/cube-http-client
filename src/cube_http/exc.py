import httpx

from .types.v1.error import V1Error
from ._utils.serde import model_parse


__all__ = ["MetaV1Error", "LoadV1Error", "SqlV1Error"]


class BaseV1Error(Exception):
    def __init__(self, status_code: int, error: str) -> None:
        self.status_code = status_code
        self.error = error
        super().__init__(str(self))

    @classmethod
    def from_response(cls, res: httpx.Response) -> "BaseV1Error":
        return cls(
            status_code=res.status_code,
            error=model_parse(V1Error, res.json()).error,
        )

    def __str__(self) -> str:
        return f"Returned status code {self.status_code}. Reason: {self.error}"


class MetaV1Error(BaseV1Error):
    pass


class LoadV1Error(BaseV1Error):
    pass


class SqlV1Error(BaseV1Error):
    pass
