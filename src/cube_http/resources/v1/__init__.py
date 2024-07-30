from functools import cached_property

from .._base import SyncApiResource, AsyncApiResource

from .load import AsyncLoad, Load
from .meta import AsyncMeta, Meta


class V1(SyncApiResource):
    @cached_property
    def meta(self) -> Meta:
        return Meta(self._client)

    @cached_property
    def load(self) -> Load:
        return Load(self._client)


class AsyncV1(AsyncApiResource):
    @cached_property
    def meta(self) -> AsyncMeta:
        return AsyncMeta(self._client)

    @cached_property
    def load(self) -> AsyncLoad:
        return AsyncLoad(self._client)
