# cube-http-client

Pythonic HTTP client for [Cube.dev](https://cube.dev) REST API (sync + async support)

## Installation

[![PyPI version](https://badge.fury.io/py/cube-http-client.svg)](https://badge.fury.io/py/cube-http-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cube-http-client.svg)](https://pypi.org/project/cube-http-client)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cube-http-client)](https://pypi.org/project/cube-http-client/)

Available on [PyPI](https://pypi.org/project/cube-http-client)

```bash
pip install cube-http-client
```

## Quickstart

```python
import cube_http

cube = cube_http.Client({"url": "...", "token": "..."})

# get metadata
meta = cube.v1.meta()

# load query results
results = cube.v1.load(
    {
        "query": {
            "measures": ["tasks.count"],
            "dimensions": ["tasks.status"],
        }
    }
)

# compile to SQL
compiled_sql_response = cube.v1.sql(
    {
        "query": {
            "measures": ["tasks.count"],
            "dimensions": ["tasks.status"],
        }
    }
)
```

## Client Configuration

Both synchronous and asynchronous clients accept the following configuration options:

```python
client_options = {
    # Required parameters
    "url": "http://localhost:4000/cubejs-api",  # Deployment base URL
    "token": "your-api-token",                  # API token for authorization

    # Optional parameters
    "timeout": 60.0,                            # Request timeout in seconds
    "max_retries": 3,                           # Number of retry attempts for failed requests
    "default_headers": {                        # Custom headers to include in every request
        "X-Custom-Header": "value"
    }
}

# Synchronous client
cube = cube_http.Client(client_options)

# Asynchronous client
cube_async = cube_http.AsyncClient(client_options)
```

You can also provide custom `httpx.Client` or `httpx.AsyncClient` instances:

```python
import httpx
import cube_http

# Custom synchronous client
http_client = httpx.Client(
    base_url="http://localhost:4000/cubejs-api",
    headers={"Authorization": "token", "Content-Type": "application/json"},
    timeout=httpx.Timeout(10.0)
)
cube = cube_http.Client({"http_client": http_client, "token": "token", "url": "http://localhost:4000/cubejs-api"})

# Custom asynchronous client
async_http_client = httpx.AsyncClient(
    base_url="http://localhost:4000/cubejs-api",
    headers={"Authorization": "token", "Content-Type": "application/json"},
    timeout=httpx.Timeout(10.0)
)
cube_async = cube_http.AsyncClient({"http_client": async_http_client, "token": "token", "url": "http://localhost:4000/cubejs-api"})
```

## Detailed Usage

### Synchronous

```python
import cube_http
from cube_http.exc import V1LoadError

# Initialize client
cube = cube_http.Client({
    "url": "http://localhost:4000/cubejs-api",
    "token": "your-api-token",
})

# Query with filters
try:
    response = cube.v1.load({
        "query": {
            "measures": ["tasks.count"],
            "dimensions": ["tasks.status"],
            "filters": [
                {
                    "member": "tasks.priority",
                    "operator": "equals",
                    "values": ["High"]
                }
            ]
        }
    })

    # Access the results
    data = response.results[0].data
    print(f"Found {len(data)} records")

except V1LoadError as e:
    print(f"Error loading data: {e}")
```

### Asynchronous

```python
import asyncio
import cube_http
from cube_http.exc import V1MetaError

async def get_metadata():
    # Initialize async client
    cube = cube_http.AsyncClient({
        "url": "http://localhost:4000/cubejs-api",
        "token": "your-api-token",
        "timeout": 30.0
    })

    try:
        # Fetch metadata
        meta_response = await cube.v1.meta()

        # Access cube definitions
        cubes = meta_response.cubes
        print(f"Available cubes: {[cube.name for cube in cubes]}")

        # Get measures and dimensions for a specific cube
        for cube in cubes:
            if cube.name == "tasks":
                print(f"Measures in tasks cube: {[m.name for m in cube.measures]}")
                print(f"Dimensions in tasks cube: {[d.name for d in cube.dimensions]}")

    except V1MetaError as e:
        print(f"Error fetching metadata: {e}")

# Run the async function
asyncio.run(get_metadata())
```

### Working with Query Responses

The client returns Pydantic models for all responses, making it easy to access response data:

```python
# Load query example
load_response = cube.v1.load({
    "query": {
        "measures": ["tasks.count"],
        "dimensions": ["tasks.status", "tasks.priority"],
        "timeDimensions": [
            {
                "dimension": "tasks.createdAt",
                "granularity": "month"
            }
        ]
    }
})

# Access query results
for result in load_response.results:
    # Get data records
    records = result.data
    for record in records:
        print(f"Status: {record['tasks.status']}, Priority: {record['tasks.priority']}, Count: {record['tasks.count']}")

    # Access annotations
    annotations = result.annotation
    measure_annotations = annotations.measures
    dimension_annotations = annotations.dimensions

    # Check for pre-aggregations usage
    if result.used_pre_aggregations:
        print("Used pre-aggregations:", result.used_pre_aggregations)
```

### Custom Response Models

You can provide custom response models to extend the default response models:

```python
from pydantic import Field
from cube_http.types.v1.load_response import V1LoadResponse, V1LoadResult

# Extend the default response model with additional fields
class CustomLoadResult(V1LoadResult):
    custom_field: str = Field(default=None, alias="customField")

class CustomLoadResponse(V1LoadResponse):
    custom_metadata: dict = Field(default_factory=dict, alias="customMetadata")

# Use the custom response model
response = cube.v1.load(
    {
        "query": {
            "measures": ["tasks.count"],
            "dimensions": ["tasks.status"],
        }
    },
    response_model=CustomLoadResponse
)

# Access custom fields
custom_metadata = response.custom_metadata
```

This feature is available for all endpoints:

```python
# For SQL endpoint
from cube_http.types.v1.sql_response import V1SqlResponse

class CustomSqlResponse(V1SqlResponse):
    extra_data: dict = Field(default_factory=dict)

sql_response = cube.v1.sql(
    {"query": {"measures": ["tasks.count"]}},
    response_model=CustomSqlResponse
)

# For Meta endpoint
from cube_http.types.v1.meta_response import V1MetaResponse

class CustomMetaResponse(V1MetaResponse):
    extended_info: dict = Field(default_factory=dict)

meta_response = cube.v1.meta(
    response_model=CustomMetaResponse
)
```

Custom response models are particularly useful when working with custom or extended Cube instances that return additional fields not covered by the default models.

### SQL Query Compilation

You can retrieve the SQL that Cube would execute:

```python
# Get SQL for a query
sql_response = cube.v1.sql({
    "query": {
        "measures": ["tasks.count"],
        "dimensions": ["tasks.status"],
        "timeDimensions": [
            {
                "dimension": "tasks.createdAt",
                "granularity": "month"
            }
        ]
    }
})

# Access the SQL query and parameters
sql_query, params = sql_response.sql.sql
print("SQL query:", sql_query)
print("SQL parameters:", params)

# Other SQL response attributes
if sql_response.sql.pre_aggregations:
    print("Pre-aggregations:", sql_response.sql.pre_aggregations)
```

### Error Handling

The client provides specific error classes for each endpoint:

```python
import cube_http
from cube_http.exc import V1LoadError, V1SqlError, V1MetaError

cube = cube_http.Client({
    "url": "http://localhost:4000/cubejs-api",
    "token": "your-api-token"
})

# Load endpoint error handling
try:
    load_response = cube.v1.load({"query": {"measures": ["invalid.measure"]}})
except V1LoadError as e:
    print(f"Load error: {e}")

# SQL endpoint error handling
try:
    sql_response = cube.v1.sql({"query": {"measures": ["invalid.measure"]}})
except V1SqlError as e:
    print(f"SQL error: {e}")

# Meta endpoint error handling
try:
    meta_response = cube.v1.meta()
except V1MetaError as e:
    print(f"Meta error: {e}")
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
