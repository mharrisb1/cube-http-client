import pytest

import cube_http


def test_get_metadata(url: str, token: str):
    cube = cube_http.Client({"url": url, "token": token})
    meta = cube.v1.meta({"extended": True})
    assert meta.cubes
    assert len(meta.cubes) > 0
    assert len([cube for cube in meta.cubes if cube.type == "cube"]) > 0
    assert len([view for view in meta.cubes if view.type == "view"]) > 0


@pytest.mark.asyncio
async def test_async_get_metadata(url: str, token: str):
    cube = cube_http.AsyncClient({"url": url, "token": token})
    meta = await cube.v1.meta()
    assert meta.cubes
    assert len(meta.cubes) > 0
    assert len([cube for cube in meta.cubes if cube.type == "cube"]) > 0
    assert len([view for view in meta.cubes if view.type == "view"]) > 0
