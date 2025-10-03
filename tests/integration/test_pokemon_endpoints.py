import httpx
import pytest

from api.main import app


@pytest.mark.asyncio
async def test_get_pokemon_list():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(name, str) for name in data)


@pytest.mark.asyncio
async def test_get_pokemon_by_name_found():
    # This test assumes at least one Pokémon exists in the DB, e.g., 'pikachu'.
    # If not, adjust the name to match your test DB.
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        list_response = await ac.get("/pokemon")
        if list_response.status_code != 200 or not list_response.json():
            pytest.skip("No Pokémon in test DB to check detail endpoint.")
        name = list_response.json()[0]
        response = await ac.get(f"/pokemon/{name}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(build, dict) for build in data)
    assert all(build["pokemon"].lower() == name.lower() for build in data)


@pytest.mark.asyncio
async def test_get_pokemon_by_name_not_found():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/pokemon/thisdoesnotexist")
    assert response.status_code == 404
    assert "not found" in response.text.lower()
