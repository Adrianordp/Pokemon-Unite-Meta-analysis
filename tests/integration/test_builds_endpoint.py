import httpx
import pytest

from api.main import app


@pytest.mark.asyncio
async def test_builds_default():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/builds")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_builds_with_all_params():
    params = {
        "week": 1,
        "id": 0,
        "relevance": "any",
        "relevance_threshold": 0.0,
        "sort_by": "moveset_item_true_pick_rate",
        "sort_order": "desc",
        "pokemon": "pikachu",
        "role": "attacker",
        "item": "XSpeed",
        "ignore_pokemon": "charizard",
        "ignore_item": "focus_band",
        "ignore_role": "defender",
        "top_n": 5,
    }
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/builds", params=params)
    assert response.status_code in (200, 404, 400)


@pytest.mark.asyncio
async def test_builds_invalid_relevance():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            "/builds", params={"relevance": "invalid_strategy"}
        )
    assert response.status_code == 400
    assert "Invalid relevance strategy" in response.text


@pytest.mark.asyncio
async def test_builds_invalid_sort_by():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/builds", params={"sort_by": "invalid_field"})
    assert response.status_code == 400
    assert "Invalid sort_by field" in response.text


@pytest.mark.asyncio
async def test_builds_id_not_found():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/builds", params={"id": 99999})
    assert response.status_code == 404
    assert "Build ID not found" in response.text
