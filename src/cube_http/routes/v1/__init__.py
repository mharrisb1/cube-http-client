from .load import AsyncLoadRoute, SyncLoadRoute
from .meta import AsyncMetaRoute, SyncMetaRoute
from .sql import AsyncSqlRoute, SyncSqlRoute


class SyncV1Routes(SyncLoadRoute, SyncMetaRoute, SyncSqlRoute): ...


class AsyncV1Routes(AsyncLoadRoute, AsyncMetaRoute, AsyncSqlRoute): ...
