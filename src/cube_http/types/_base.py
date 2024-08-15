from typing import Dict

import httpx
from pydantic import BaseModel

from .._utils.serde import model_dict, model_parse


class RequestModel(BaseModel):
    def as_request_body(self) -> Dict[str, str]:
        return model_dict(self, exclude_none=True, by_alias=True)


class ResponseModel(BaseModel):
    @classmethod
    def from_response(cls, res: httpx.Response):
        return model_parse(cls, res.json())
