import httpx
from pydantic import BaseModel, ConfigDict


class ResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    @classmethod
    def from_response(cls, res: httpx.Response):
        return cls.model_validate(res.json())
