from typing import TypeVar

from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)
