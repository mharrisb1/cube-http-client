import os

import pytest

import cube_http


def test_get_metadata():
    cube = cube_http.Client(
        {
            "url": os.getenv("CUBEJS_API_URL", "NOT FOUND"),
            "token": os.getenv("CUBEJS_API_TOKEN", "NOT FOUND"),
        }
    )
    meta = cube.v1.meta(extended=True)
    assert meta.cubes
    assert len(meta.cubes) > 0


@pytest.mark.asyncio
async def test_async_get_metadata():
    cube = cube_http.AsyncClient(
        {
            "url": os.getenv("CUBEJS_API_URL", "NOT FOUND"),
            "token": os.getenv("CUBEJS_API_TOKEN", "NOT FOUND"),
        }
    )
    meta = await cube.v1.meta()
    assert meta.cubes
    assert len(meta.cubes) > 0
