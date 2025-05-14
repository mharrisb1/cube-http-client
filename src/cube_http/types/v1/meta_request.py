from typing import TypedDict
from typing_extensions import NotRequired


class V1MetaRequest(TypedDict):
    extended: NotRequired[bool]
    """Include extended fields in meta"""
