from typing import Generic, Mapping, TypedDict, Union
from typing_extensions import Required, NotRequired

import httpx

from ..types._generics import THttpClient


class ClientOptions(TypedDict, Generic[THttpClient]):
    token: Required[str]
    """API token used to authorize requests and determine SQL database you're accessing"""

    url: Required[str]
    """Deployment base URL"""

    timeout: NotRequired[Union[float, httpx.Timeout]]
    """Timeout configuration to use when sending requests"""

    max_retries: NotRequired[int]
    """Maximum number of retries to attempt on failed requests. Defaults to 0 for no retries"""

    default_headers: NotRequired[Mapping[str, str]]
    """Default headers to add to every request"""

    http_client: NotRequired[THttpClient]
    """Optional HTTPX client to use for requests"""
