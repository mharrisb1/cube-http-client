import os

import pytest

import cube_http


def test_load_query():
    cube = cube_http.Client(
        {
            "url": os.getenv("CUBEJS_API_URL", "NOT FOUND"),
            "token": os.getenv("CUBEJS_API_TOKEN", "NOT FOUND"),
        }
    )
    cube.v1.load(
        {
            "measures": ["teams.count"],
            "dimensions": ["teams.is_business_domain"],
            "limit": 10,
            "timeDimensions": [
                {
                    "dimension": "teams.team_created_at",
                    "dateRange": "last 3 month",
                    "granularity": "week",
                }
            ],
            "order": [["teams.team_id", "asc"]],
        },
    )


@pytest.mark.asyncio
async def test_async_load_query():
    cube = cube_http.AsyncClient(
        {
            "url": os.getenv("CUBEJS_API_URL", "NOT FOUND"),
            "token": os.getenv("CUBEJS_API_TOKEN", "NOT FOUND"),
        }
    )
    await cube.v1.load(
        {
            "measures": ["teams.count"],
            "dimensions": ["teams.is_business_domain"],
            "limit": 10,
            "timeDimensions": [
                {
                    "dimension": "teams.team_created_at",
                    "dateRange": "last 3 month",
                    "granularity": "week",
                }
            ],
            "order": [["teams.team_id", "asc"]],
        },
    )
