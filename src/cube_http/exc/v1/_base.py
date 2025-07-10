from json.decoder import JSONDecodeError

import httpx
from pydantic import BaseModel, ValidationError


class V1Error(BaseModel):
    error: str


class V1BaseError(Exception):
    def __init__(self, status_code: int, error: str) -> None:
        self.status_code = status_code
        self.error = error
        super().__init__(str(self))

    @classmethod
    def from_response(cls, res: httpx.Response) -> "V1BaseError":
        try:
            error = V1Error.model_validate(res.json()).error
        except ValidationError:
            error = "Invalid response from server"
        except JSONDecodeError:
            error = res.text

        return cls(status_code=res.status_code, error=error)

    def __str__(self) -> str:
        return f"Returned status code {self.status_code}. Reason: {self.error}"
