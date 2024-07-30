from typing import Mapping, TypedDict, Union
from typing_extensions import Required

import httpx


class BaseClientOptions(TypedDict, total=False):
    token: Required[str]
    """API token used to authorize requests and determine SQL database you're accessing"""

    url: Required[str]
    """Deployment base URL"""

    timeout: Union[float, httpx.Timeout]
    """Timeout configuration to use when sending requests"""

    max_retries: int
    """Maximum number of retries to attempt on failed requests. Defaults to 0 for no retries"""

    default_headers: Mapping[str, str]
    """Default headers to add to every request"""


class ClientOptions(BaseClientOptions, total=False):
    http_client: httpx.Client
    """Optional HTTPX client to use for requests"""


class AsyncClientOptions(BaseClientOptions, total=False):
    http_client: httpx.AsyncClient
    """Optional HTTPX client to use for requests"""
