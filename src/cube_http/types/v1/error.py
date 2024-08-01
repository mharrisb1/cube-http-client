from pydantic import BaseModel


class V1Error(BaseModel):
    error: str
