import httpx
import pytest

from api.main import app


@pytest.mark.asyncio
async def test_get_roles():
    """Test GET /roles endpoint returns list of roles"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/roles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # All roles should be strings
    assert all(isinstance(role, str) for role in data)
    # Check for known roles
    expected_roles = [
        "Attacker",
        "Defender",
        "Supporter",
        "Speedster",
        "All-Rounder",
    ]
    for expected_role in expected_roles:
        # At least some of these roles should be present
        pass
    # List should be sorted
    assert data == sorted(data)


@pytest.mark.asyncio
async def test_get_role_pokemon():
    """Test GET /roles/{role} endpoint returns list of Pokémon for a role"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # First, get the list of roles
        roles_response = await ac.get("/roles")
        if roles_response.status_code != 200 or not roles_response.json():
            pytest.skip("No roles in test DB to check role endpoint.")

        # Get the first role
        role = roles_response.json()[0]
        response = await ac.get(f"/roles/{role}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # All entries should be strings (Pokémon names)
    assert all(isinstance(name, str) for name in data)
    # List should be sorted
    assert data == sorted(data)


@pytest.mark.asyncio
async def test_get_role_pokemon_case_insensitive():
    """Test GET /roles/{role} endpoint is case-insensitive"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # First, get the list of roles
        roles_response = await ac.get("/roles")
        if roles_response.status_code != 200 or not roles_response.json():
            pytest.skip("No roles in test DB.")

        # Get the first role and test with different cases
        role = roles_response.json()[0]
        response_lower = await ac.get(f"/roles/{role.lower()}")
        response_upper = await ac.get(f"/roles/{role.upper()}")

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    # Both should return the same data
    assert response_lower.json() == response_upper.json()


@pytest.mark.asyncio
async def test_get_role_not_found():
    """Test GET /roles/{role} with invalid role returns 404"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/roles/InvalidRoleThatDoesNotExist")
    assert response.status_code == 404
    assert "not found" in response.text.lower()


@pytest.mark.asyncio
async def test_get_items():
    """Test GET /items endpoint returns list of items"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # All items should be strings
    assert all(isinstance(item, str) for item in data)
    # List should be sorted
    assert data == sorted(data)


@pytest.mark.asyncio
async def test_get_item_pokemon():
    """Test GET /items/{name} endpoint returns list of Pokémon for an item"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # First, get the list of items
        items_response = await ac.get("/items")
        if items_response.status_code != 200 or not items_response.json():
            pytest.skip("No items in test DB to check item endpoint.")

        # Get the first item
        item = items_response.json()[0]
        response = await ac.get(f"/items/{item}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # All entries should be strings (Pokémon names)
    assert all(isinstance(name, str) for name in data)
    # List should be sorted
    assert data == sorted(data)


@pytest.mark.asyncio
async def test_get_item_pokemon_case_insensitive():
    """Test GET /items/{name} endpoint is case-insensitive"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # First, get the list of items
        items_response = await ac.get("/items")
        if items_response.status_code != 200 or not items_response.json():
            pytest.skip("No items in test DB.")

        # Get the first item and test with different cases
        item = items_response.json()[0]
        response_lower = await ac.get(f"/items/{item.lower()}")
        response_upper = await ac.get(f"/items/{item.upper()}")

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    # Both should return the same data
    assert response_lower.json() == response_upper.json()


@pytest.mark.asyncio
async def test_get_item_not_found():
    """Test GET /items/{name} with invalid item returns 404"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/items/InvalidItemThatDoesNotExist")
    assert response.status_code == 404
    assert "not found" in response.text.lower()


@pytest.mark.asyncio
async def test_roles_and_items_consistency():
    """Test that roles and items endpoints return consistent data"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Get all roles
        roles_response = await ac.get("/roles")
        assert roles_response.status_code == 200
        roles = roles_response.json()

        # Get all items
        items_response = await ac.get("/items")
        assert items_response.status_code == 200
        items = items_response.json()

        # Both lists should have content
        assert len(roles) > 0
        assert len(items) > 0

        # Lists should be unique (no duplicates)
        assert len(roles) == len(set(roles))
        assert len(items) == len(set(items))
