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
        query={
            "measures": ["teams.count"],
            "dimensions": ["teams.team_domain"],
        },
    )


@pytest.mark.asyncio
async def test_async_get_metadata():
    cube = cube_http.AsyncClient(
        {
            "url": os.getenv("CUBEJS_API_URL", "NOT FOUND"),
            "token": os.getenv("CUBEJS_API_TOKEN", "NOT FOUND"),
        }
    )
    await cube.v1.load(
        query={
            "measures": ["teams.count"],
            "dimensions": ["teams.team_domain"],
        },
    )
