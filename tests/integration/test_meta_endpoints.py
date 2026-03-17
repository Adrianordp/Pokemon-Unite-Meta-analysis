import httpx
import pytest

from api.main import app


@pytest.mark.asyncio
async def test_get_ids():
    """Test GET /ids endpoint returns list of build IDs"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ids")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # All IDs should be integers
    assert all(isinstance(id, int) for id in data)


@pytest.mark.asyncio
async def test_get_weeks():
    """Test GET /weeks endpoint returns list of weeks"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/weeks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # All weeks should be strings
    assert all(isinstance(week, str) for week in data)


@pytest.mark.asyncio
async def test_get_filters():
    """Test GET /filters endpoint returns list of filter strategies"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check that all filters have required fields
    for filter_strategy in data:
        assert "name" in filter_strategy
        assert "description" in filter_strategy
        assert "type" in filter_strategy
        assert filter_strategy["type"] in ["include", "exclude"]
    # Check that known filters are present
    filter_names = [f["name"] for f in data]
    assert "pokemon" in filter_names
    assert "role" in filter_names
    assert "item" in filter_names
    assert "ignore_pokemon" in filter_names
    assert "ignore_role" in filter_names
    assert "ignore_item" in filter_names


@pytest.mark.asyncio
async def test_get_filter_pokemon():
    """Test GET /filters/{filter_name} for 'pokemon' filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "pokemon"
    assert data["type"] == "include"
    assert "description" in data
    assert "parameter" in data
    assert "value_format" in data
    assert "example" in data
    assert "usage" in data


@pytest.mark.asyncio
async def test_get_filter_role():
    """Test GET /filters/{filter_name} for 'role' filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/role")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "role"
    assert data["type"] == "include"
    assert "available_values" in data
    assert isinstance(data["available_values"], list)
    assert "Attacker" in data["available_values"]


@pytest.mark.asyncio
async def test_get_filter_item():
    """Test GET /filters/{filter_name} for 'item' filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/item")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "item"
    assert data["type"] == "include"


@pytest.mark.asyncio
async def test_get_filter_ignore_pokemon():
    """Test GET /filters/{filter_name} for 'ignore_pokemon' filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/ignore_pokemon")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "ignore_pokemon"
    assert data["type"] == "exclude"


@pytest.mark.asyncio
async def test_get_filter_ignore_role():
    """Test GET /filters/{filter_name} for 'ignore_role' filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/ignore_role")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "ignore_role"
    assert data["type"] == "exclude"
    assert "available_values" in data


@pytest.mark.asyncio
async def test_get_filter_ignore_item():
    """Test GET /filters/{filter_name} for 'ignore_item' filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/ignore_item")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "ignore_item"
    assert data["type"] == "exclude"


@pytest.mark.asyncio
async def test_get_filter_not_found():
    """Test GET /filters/{filter_name} with invalid filter"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/filters/invalid_filter")
    assert response.status_code == 404
    assert "not found" in response.text.lower()


@pytest.mark.asyncio
async def test_get_logs():
    """Test GET /logs endpoint returns log information"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/logs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "available_logs" in data
    assert "description" in data
    assert isinstance(data["available_logs"], list)
    # Each log entry should have specific fields
    for log_entry in data["available_logs"]:
        assert "name" in log_entry
        assert "path" in log_entry
