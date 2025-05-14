from typing import Literal, TypedDict
from typing_extensions import NotRequired, Required

from .load_request import V1LoadRequestQuery


class V1SqlRequest(TypedDict):
    format: NotRequired[Literal["sql", "rest"]]
    """
    Query format:
    sql for SQL API queries,
    rest for REST API queries (default) 
    """

    query: Required[V1LoadRequestQuery]
    """Query as an URL-encoded JSON object or SQL query"""

    disable_post_processing: NotRequired[bool]
    """Flag that affects query planning"""
