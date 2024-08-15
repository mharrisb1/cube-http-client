# cube-http-client

Pythonic HTTP client for [Cube.dev](https://cube.dev) REST API (sync + async support)

## Installation

```sh
pip install cube-http-client
```

## Quickstart

```python
import cube_http

cube = cube_http.Client({"url": "...", "token": "..."})

# get metadata
meta = cube.v1.meta()

# load query results
results = cube.v1.load({
    "measures": ["..."],
    "dimensions": ["..."],
})

# compile to SQL
compiled_sql = cube.v1.sql({
    "measures": ["..."],
    "dimensions": ["..."],
})
```

## Support Coverage

| Endpoint                    | Description                                                                                                                                                               | Supported? |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `/v1/load`                  | Get the data for a query.                                                                                                                                                 | ✅         |
| `/v1/sql`                   | Get the SQL Code generated by Cube to be executed in the database.                                                                                                        | ✅         |
| `/v1/meta`                  | Get meta-information for cubes and views defined in the data model. Information about cubes and views with `public: false` will not be returned.                          | ✅         |
| `/v1/run-scheduled-refresh` | Trigger a scheduled refresh run to refresh pre-aggregations.                                                                                                              | ❌         |
| `/v1/pre-aggregations/jobs` | Trigger pre-aggregation build jobs or retrieve statuses of such jobs.                                                                                                     | ❌         |
| `/readyz`                   | Returns the ready state of the deployment.                                                                                                                                | ❌         |
| `/livez`                    | Returns the liveness state of the deployment. This is confirmed by testing any existing connections to dataSource. If no connections exist, it will report as successful. | ❌         |

## Usage

### Synchronous

```python
import cube_http

cube = cube_http.Client(...)
```

### Asynchronous

```python
import cube_http

cube = cube_http.AsyncClient(...)
```

### Error handling

Error classes are available for each endpoint. For example, handling an API error when calling `/v1/meta` endpoint:

```python
import cube_http
from cube_http.exc.v1 import V1MetaError

cube = cube_http.Client(...)

try:
    meta = cube.v1.meta()
except V1MetaError as e:
    print(e)
```
