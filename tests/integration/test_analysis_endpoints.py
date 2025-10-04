import httpx
import pytest

from api.main import app


@pytest.mark.asyncio
async def test_get_relevance_strategies():
    """Test GET /relevance endpoint returns list of strategies"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check that all strategies have required fields
    for strategy in data:
        assert "name" in strategy
        assert "description" in strategy
    # Check that known strategies are present
    strategy_names = [s["name"] for s in data]
    assert "any" in strategy_names
    assert "percentage" in strategy_names
    assert "top_n" in strategy_names
    assert "cumulative_coverage" in strategy_names
    assert "quartile" in strategy_names


@pytest.mark.asyncio
async def test_get_relevance_strategy_any():
    """Test GET /relevance/{strategy} for 'any' strategy"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance/any")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "any"
    assert "description" in data
    assert "threshold_type" in data
    assert "threshold_description" in data


@pytest.mark.asyncio
async def test_get_relevance_strategy_percentage():
    """Test GET /relevance/{strategy} for 'percentage' strategy"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance/percentage")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "percentage"
    assert data["threshold_type"] == "percentage"


@pytest.mark.asyncio
async def test_get_relevance_strategy_top_n():
    """Test GET /relevance/{strategy} for 'top_n' strategy"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance/top_n")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "top_n"
    assert data["threshold_type"] == "integer"


@pytest.mark.asyncio
async def test_get_relevance_strategy_cumulative_coverage():
    """Test GET /relevance/{strategy} for 'cumulative_coverage' strategy"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance/cumulative_coverage")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "cumulative_coverage"
    assert data["threshold_type"] == "percentage"


@pytest.mark.asyncio
async def test_get_relevance_strategy_quartile():
    """Test GET /relevance/{strategy} for 'quartile' strategy"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance/quartile")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "quartile"
    assert data["threshold_type"] == "quartile"


@pytest.mark.asyncio
async def test_get_relevance_strategy_not_found():
    """Test GET /relevance/{strategy} with invalid strategy"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/relevance/invalid_strategy")
    assert response.status_code == 404
    assert "not found" in response.text.lower()


@pytest.mark.asyncio
async def test_get_sort_criteria():
    """Test GET /sort_by endpoint returns list of sort criteria"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/sort_by")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check that all criteria have required fields
    for criteria in data:
        assert "name" in criteria
        assert "description" in criteria
        assert "default_order" in criteria
    # Check that known criteria are present
    criteria_names = [c["name"] for c in data]
    assert "pokemon" in criteria_names
    assert "role" in criteria_names
    assert "pokemon_win_rate" in criteria_names
    assert "moveset_item_win_rate" in criteria_names
    assert "moveset_item_true_pick_rate" in criteria_names


@pytest.mark.asyncio
async def test_get_sort_criteria_pokemon():
    """Test GET /sort_by/{criteria} for 'pokemon' criteria"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/sort_by/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "pokemon"
    assert "description" in data
    assert "field_type" in data
    assert data["field_type"] == "string"
    assert data["default_order"] == "asc"


@pytest.mark.asyncio
async def test_get_sort_criteria_pokemon_win_rate():
    """Test GET /sort_by/{criteria} for 'pokemon_win_rate' criteria"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/sort_by/pokemon_win_rate")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "pokemon_win_rate"
    assert data["field_type"] == "float"
    assert data["default_order"] == "desc"


@pytest.mark.asyncio
async def test_get_sort_criteria_moveset_item_true_pick_rate():
    """Test GET /sort_by/{criteria} for 'moveset_item_true_pick_rate' criteria"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/sort_by/moveset_item_true_pick_rate")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["name"] == "moveset_item_true_pick_rate"
    assert data["field_type"] == "float"
    assert data["default_order"] == "desc"


@pytest.mark.asyncio
async def test_get_sort_criteria_not_found():
    """Test GET /sort_by/{criteria} with invalid criteria"""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/sort_by/invalid_criteria")
    assert response.status_code == 404
    assert "not found" in response.text.lower()
