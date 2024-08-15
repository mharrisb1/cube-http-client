from typing import TypeVar, Union

from pydantic import BaseModel
from httpx import Client, AsyncClient

__all__ = ["THttpClient", "TModel"]

TModel = TypeVar("TModel", bound=BaseModel)

THttpClient = TypeVar("THttpClient", bound=Union[Client, AsyncClient])
