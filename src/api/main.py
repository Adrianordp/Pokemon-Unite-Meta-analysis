from typing import List

from fastapi import Depends, FastAPI, HTTPException, Path

from api.config import settings
from api.custom_log import LOG
from entity.build_model import BuildModel
from entity.build_response import BuildResponse
from entity.builds_query_params import BuildsQueryParams
from pokemon_unite_meta_analysis.filter_strategy import FILTER_STRATEGIES
from pokemon_unite_meta_analysis.relevance_strategy import (
    RELEVANCE_STRATEGIES,
    Relevance,
)
from pokemon_unite_meta_analysis.sort_strategy import SORT_STRATEGIES, SortBy
from repository.build_repository import BuildRepository

app = FastAPI(title=settings.api_name, debug=settings.debug)


def _calculate_popularity_ranks(
    builds: List[BuildModel], week: str = None
) -> dict[int, int]:
    """
    Calculate popularity ranks for builds based on moveset_item_true_pick_rate.

    Args:
        builds: List of builds to calculate popularity for
        week: Optional week filter for calculating popularity within a week

    Returns:
        Dictionary mapping build ID to popularity rank (1 = most popular)
    """
    # Get all builds for the week to calculate popularity
    with BuildRepository() as repo:
        week_builds = repo.get_all_builds(week=week)

    # Sort by moveset_item_true_pick_rate descending to get popularity order
    sorted_by_popularity = sorted(
        week_builds, key=lambda b: b.moveset_item_true_pick_rate, reverse=True
    )

    # Create mapping of build ID to popularity rank
    popularity_map = {
        build.id: idx + 1 for idx, build in enumerate(sorted_by_popularity)
    }

    return popularity_map


def _convert_to_build_response(
    builds: List[BuildModel], week: str = None
) -> List[BuildResponse]:
    """
    Convert BuildModel instances to BuildResponse with computed fields.

    Args:
        builds: List of BuildModel instances from database
        week: Optional week for popularity calculation

    Returns:
        List of BuildResponse instances with popularity and rank fields
    """
    # Calculate popularity ranks for all builds in the week
    popularity_map = _calculate_popularity_ranks(builds, week)

    # Convert to BuildResponse with rank (position in current result set)
    # and popularity (position within week by moveset_item_true_pick_rate)
    responses = []
    for idx, build in enumerate(builds):
        responses.append(
            BuildResponse(
                id=build.id,
                week=build.week,
                pokemon=build.pokemon,
                role=build.role,
                pokemon_win_rate=build.pokemon_win_rate,
                pokemon_pick_rate=build.pokemon_pick_rate,
                move_1=build.move_1,
                move_2=build.move_2,
                moveset_win_rate=build.moveset_win_rate,
                moveset_pick_rate=build.moveset_pick_rate,
                moveset_true_pick_rate=build.moveset_true_pick_rate,
                item=build.item,
                moveset_item_win_rate=build.moveset_item_win_rate,
                moveset_item_pick_rate=build.moveset_item_pick_rate,
                moveset_item_true_pick_rate=build.moveset_item_true_pick_rate,
                popularity=popularity_map.get(build.id, 0),
                rank=idx + 1,
            )
        )

    return responses


# /pokemon endpoints
@app.get(
    "/pokemon",
    response_model=List[str],
    summary="Get list of available Pokémon",
    description="Returns a list of all unique Pokémon names in the builds database.",
)
def get_pokemon():
    with BuildRepository() as repo:
        pokemons = repo.get_all_pokemons_by_table("builds")
    # Remove duplicates and sort
    return sorted(list(set(pokemons)))


@app.get(
    "/pokemon/{name}",
    response_model=List[BuildResponse],
    summary="Get all builds for a specific Pokémon",
    description="Returns all builds for the specified Pokémon name.",
)
def get_pokemon_by_name(name: str = Path(..., description="Pokémon name")):
    with BuildRepository() as repo:
        builds = repo.get_all_builds()
    filtered = [
        build for build in builds if build.pokemon.lower() == name.lower()
    ]
    if not filtered:
        raise HTTPException(
            status_code=404, detail=f"Pokémon '{name}' not found."
        )
    return _convert_to_build_response(filtered)


# /roles endpoints
@app.get(
    "/roles",
    response_model=List[str],
    summary="Get list of available roles",
    description="Returns a list of all unique roles in the builds database.",
)
def get_roles():
    """Get list of available roles"""
    LOG.info("get_roles")
    with BuildRepository() as repo:
        builds = repo.get_all_builds()
    roles = [build.role for build in builds]
    # Remove duplicates and sort
    return sorted(list(set(roles)))


@app.get(
    "/roles/{role}",
    response_model=List[str],
    summary="Get list of Pokémon for a specific role",
    description="Returns a list of unique Pokémon names that have the specified role.",
)
def get_role_pokemon(role: str = Path(..., description="Role name")):
    """Get list of Pokémon for a specific role"""
    LOG.info("get_role_pokemon")
    LOG.debug("role: %s", role)

    with BuildRepository() as repo:
        builds = repo.get_all_builds()

    # Filter builds by role (case-insensitive)
    filtered = [build for build in builds if build.role.lower() == role.lower()]

    if not filtered:
        raise HTTPException(status_code=404, detail=f"Role '{role}' not found.")

    # Get unique Pokémon names for this role
    pokemon_names = [build.pokemon for build in filtered]
    return sorted(list(set(pokemon_names)))


# /items endpoints
@app.get(
    "/items",
    response_model=List[str],
    summary="Get list of available items",
    description="Returns a list of all unique items in the builds database.",
)
def get_items():
    """Get list of available items"""
    LOG.info("get_items")
    with BuildRepository() as repo:
        builds = repo.get_all_builds()
    items = [build.item for build in builds]
    # Remove duplicates and sort
    return sorted(list(set(items)))


@app.get(
    "/items/{name}",
    response_model=List[str],
    summary="Get list of Pokémon that use a specific item",
    description="Returns a list of unique Pokémon names that use the specified item.",
)
def get_item_pokemon(name: str = Path(..., description="Item name")):
    """Get list of Pokémon that use a specific item"""
    LOG.info("get_item_pokemon")
    LOG.debug("name: %s", name)

    with BuildRepository() as repo:
        builds = repo.get_all_builds()

    # Filter builds by item (case-insensitive)
    filtered = [build for build in builds if build.item.lower() == name.lower()]

    if not filtered:
        raise HTTPException(status_code=404, detail=f"Item '{name}' not found.")

    # Get unique Pokémon names that use this item
    pokemon_names = [build.pokemon for build in filtered]
    return sorted(list(set(pokemon_names)))


@app.get(
    "/",
    summary="API root endpoint",
    description="""
Returns a welcome message and basic API metadata (name, debug status, host, port).
Useful for confirming the API is running and retrieving configuration info.

**Response:**
- `message` (str): Welcome message with API name.
- `debug` (bool): Debug mode status.
- `host` (str): Host address.
- `port` (int): Port number.
    """,
)
def read_root():
    LOG.info("read_root")
    return {
        "message": f"{settings.api_name} is running.",
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
    }


# Health check endpoint
@app.get(
    "/health",
    summary="Health check endpoint",
    description="""
    Returns the health status of the API. Useful for monitoring and readiness/liveness probes.
    
**Response:**
- `status` (str): Always returns `ok` if the API is running.
    """,
)
def health_check():
    LOG.info("health_check")
    return {"status": "ok"}


@app.get(
    "/weeks",
    response_model=List[str],
    summary="Get available weeks",
    description="Returns a list of available weeks for which builds are stored.",
)
def get_weeks():
    """Get list of available weeks"""
    with BuildRepository() as repo:
        return repo.get_available_weeks()


# /builds endpoint with improved validation and error handling
@app.get(
    "/builds",
    response_model=List[BuildResponse],
    summary="Retrieve builds with filtering, sorting, and relevance options",
    description="""
Returns a list of Pokémon Unite builds, with options for filtering, sorting, and relevance strategies.
    
**Query Parameters:**
- `week` (int, optional): Week number for filtering builds.
- `id` (int, optional): Build ID for direct lookup.
- `relevance` (str, optional): Relevance strategy:
    - `any`
    - `percentage`
    - `top_n`
    - `cumulative_coverage`
    - `quartile`
- `relevance_threshold` (float, optional): Threshold for relevance filtering.
- `sort_by` (str, optional): Field to sort by. Options:
    - `pokemon`
    - `role`
    - `pokemon_win_rate`
    - `pokemon_pick_rate`
    - `moveset_win_rate`
    - `moveset_pick_rate`
    - `moveset_true_pick_rate`
    - `item`
    - `moveset_item_win_rate`
    - `moveset_item_pick_rate`
    - `moveset_item_true_pick_rate`
- `sort_order` (str, optional): Sort order:
    - `asc`
    - `desc`
- `pokemon` (str, optional): Filter by Pokémon name.
- `role` (str, optional): Filter by role. Options:
    - `All-Rounder`
    - `Attacker`
    - `Defender`
    - `Supporter`
    - `Speedster`
- `item` (str, optional): Filter by item. Options:
    - `Potion`
    - `EjectButton`
    - `XAttack`
    - `XSpeed`
    - `Tail`
    - `ShedinjaDoll`
    - `Purify` (full-heal)
    - `Gear` (slow-smoke)
    - `Ganrao` (goal getter)
    - `???` (goal hacker)
- `ignore_pokemon` (str, optional): Exclude Pokémon name.
- `ignore_item` (str, optional): Exclude item.
- `ignore_role` (str, optional): Exclude role.

**Response:**
- List of builds, each with Pokémon, role, win/pick rates, moves, item, and more. See `BuildResponse` model for details.
    """,
)
def get_builds(params: BuildsQueryParams = Depends()):
    LOG.info("get_builds")
    LOG.debug("week: %s", params.week)
    LOG.debug("id: %s", params.id)
    LOG.debug("relevance: %s", params.relevance)
    LOG.debug("relevance_threshold: %s", params.relevance_threshold)
    LOG.debug("sort_by: %s", params.sort_by)
    LOG.debug("sort_order: %s", params.sort_order)
    LOG.debug("pokemon: %s", params.pokemon)
    LOG.debug("role: %s", params.role)
    LOG.debug("item: %s", params.item)
    LOG.debug("ignore_pokemon: %s", params.ignore_pokemon)
    LOG.debug("ignore_item: %s", params.ignore_item)
    LOG.debug("ignore_role: %s", params.ignore_role)
    LOG.debug("top_n: %s", params.top_n)

    with BuildRepository() as repo:
        week = None

        if params.week is not None:
            available_weeks = repo.get_available_weeks()
            if params.week not in available_weeks:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid week: {params.week}. Available weeks: {available_weeks}",
                )
            week = params.week

        all_builds = repo.get_all_builds(week=week)

    builds = all_builds.copy()

    # Direct ID lookup
    if params.id is not None:
        if params.id < 0 or params.id >= len(builds):
            raise HTTPException(status_code=404, detail="Build ID not found")
        return _convert_to_build_response([builds[params.id]], week)

    # Validate and map relevance
    try:
        relevance_enum = Relevance(params.relevance)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid relevance strategy: {params.relevance}",
        )

    # Apply relevance strategy
    builds = RELEVANCE_STRATEGIES[relevance_enum].apply(
        builds, params.relevance_threshold, lambda: all_builds
    )

    # Apply filter strategies
    if params.pokemon:
        builds = FILTER_STRATEGIES["pokemon"].apply(builds, params.pokemon)
    elif params.ignore_pokemon:
        builds = FILTER_STRATEGIES["ignore_pokemon"].apply(
            builds, params.ignore_pokemon
        )

    if params.role:
        builds = FILTER_STRATEGIES["role"].apply(builds, params.role)
    elif params.ignore_role:
        builds = FILTER_STRATEGIES["ignore_role"].apply(
            builds, params.ignore_role
        )

    if params.item:
        builds = FILTER_STRATEGIES["item"].apply(builds, params.item)
    elif params.ignore_item:
        builds = FILTER_STRATEGIES["ignore_item"].apply(
            builds, params.ignore_item
        )

    # Validate and map sort_by
    try:
        sort_by_enum = SortBy(params.sort_by)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid sort_by field: {params.sort_by}"
        )

    reverse = params.sort_order == "desc"
    builds = SORT_STRATEGIES[sort_by_enum.value].apply(builds, reverse=reverse)

    # Limit to top_n results if specified
    if params.top_n is not None and params.top_n > 0:
        builds = builds[: params.top_n]

    # Convert to response model with computed popularity and rank fields
    return _convert_to_build_response(builds, week)


# /relevance endpoints
@app.get(
    "/relevance",
    response_model=List[dict],
    summary="Get list of available relevance strategies",
    description="Returns a list of all available relevance strategies with their descriptions.",
)
def get_relevance_strategies():
    """Get list of available relevance strategies"""
    LOG.info("get_relevance_strategies")
    return [
        {
            "name": Relevance.ANY.value,
            "description": "Returns all builds without filtering.",
        },
        {
            "name": Relevance.PERCENTAGE.value,
            "description": "Filters builds with moveset_item_true_pick_rate >= threshold (0-100).",
        },
        {
            "name": Relevance.TOP_N.value,
            "description": "Returns top N builds based on moveset_item_true_pick_rate.",
        },
        {
            "name": Relevance.CUMULATIVE_COVERAGE.value,
            "description": "Returns builds until cumulative moveset_item_true_pick_rate >= threshold (0-100).",
        },
        {
            "name": Relevance.QUARTILE.value,
            "description": "Returns builds from the top N quartiles (threshold: 1-4).",
        },
    ]


@app.get(
    "/relevance/{strategy}",
    response_model=dict,
    summary="Get details about a specific relevance strategy",
    description="Returns detailed information about the specified relevance strategy.",
)
def get_relevance_strategy(
    strategy: str = Path(..., description="Relevance strategy name"),
):
    """Get details about a specific relevance strategy"""
    LOG.info("get_relevance_strategy")
    LOG.debug("strategy: %s", strategy)

    # Validate strategy
    try:
        relevance_enum = Relevance(strategy)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Relevance strategy '{strategy}' not found.",
        )

    strategies_info = {
        Relevance.ANY: {
            "name": Relevance.ANY.value,
            "description": "Returns all builds without filtering.",
            "threshold_type": "none",
            "threshold_description": "Threshold is ignored for this strategy.",
        },
        Relevance.PERCENTAGE: {
            "name": Relevance.PERCENTAGE.value,
            "description": "Filters builds with moveset_item_true_pick_rate >= threshold.",
            "threshold_type": "percentage",
            "threshold_description": "Threshold should be a value between 0 and 100 representing the minimum pick rate percentage.",
        },
        Relevance.TOP_N: {
            "name": Relevance.TOP_N.value,
            "description": "Returns top N builds based on moveset_item_true_pick_rate.",
            "threshold_type": "integer",
            "threshold_description": "Threshold should be a positive integer representing the number of top builds to return.",
        },
        Relevance.CUMULATIVE_COVERAGE: {
            "name": Relevance.CUMULATIVE_COVERAGE.value,
            "description": "Returns builds until cumulative moveset_item_true_pick_rate >= threshold.",
            "threshold_type": "percentage",
            "threshold_description": "Threshold should be a value between 0 and 100 representing the cumulative coverage percentage.",
        },
        Relevance.QUARTILE: {
            "name": Relevance.QUARTILE.value,
            "description": "Returns builds from the top N quartiles based on moveset_item_true_pick_rate.",
            "threshold_type": "quartile",
            "threshold_description": "Threshold should be 1, 2, 3, or 4 representing the number of quartiles to include (1 = top 25%, 2 = top 50%, etc.).",
        },
    }

    return strategies_info[relevance_enum]


# /sort_by endpoints
@app.get(
    "/sort_by",
    response_model=List[dict],
    summary="Get list of available sort criteria",
    description="Returns a list of all available sort criteria for builds.",
)
def get_sort_criteria():
    """Get list of available sort criteria"""
    LOG.info("get_sort_criteria")
    return [
        {
            "name": SortBy.POKEMON.value,
            "description": "Sort by Pokémon name (alphabetically).",
            "default_order": "asc",
        },
        {
            "name": SortBy.ROLE.value,
            "description": "Sort by role (alphabetically).",
            "default_order": "asc",
        },
        {
            "name": SortBy.POKEMON_WIN_RATE.value,
            "description": "Sort by Pokémon win rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.POKEMON_PICK_RATE.value,
            "description": "Sort by Pokémon pick rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.MOVESET_WIN_RATE.value,
            "description": "Sort by moveset win rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.MOVESET_PICK_RATE.value,
            "description": "Sort by moveset pick rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.MOVESET_TRUE_PICK_RATE.value,
            "description": "Sort by moveset true pick rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.ITEM.value,
            "description": "Sort by item name (alphabetically).",
            "default_order": "asc",
        },
        {
            "name": SortBy.MOVESET_ITEM_WIN_RATE.value,
            "description": "Sort by moveset item win rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.MOVESET_ITEM_PICK_RATE.value,
            "description": "Sort by moveset item pick rate.",
            "default_order": "desc",
        },
        {
            "name": SortBy.MOVESET_ITEM_TRUE_PICK_RATE.value,
            "description": "Sort by moveset item true pick rate.",
            "default_order": "desc",
        },
    ]


@app.get(
    "/sort_by/{criteria}",
    response_model=dict,
    summary="Get details about a specific sort criteria",
    description="Returns detailed information about the specified sort criteria.",
)
def get_sort_criteria_details(
    criteria: str = Path(..., description="Sort criteria name"),
):
    """Get details about a specific sort criteria"""
    LOG.info("get_sort_criteria_details")
    LOG.debug("criteria: %s", criteria)

    # Validate criteria
    try:
        sort_by_enum = SortBy(criteria)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Sort criteria '{criteria}' not found.",
        )

    criteria_info = {
        SortBy.POKEMON: {
            "name": SortBy.POKEMON.value,
            "description": "Sort builds by Pokémon name (alphabetically).",
            "field_type": "string",
            "default_order": "asc",
        },
        SortBy.ROLE: {
            "name": SortBy.ROLE.value,
            "description": "Sort builds by role (alphabetically).",
            "field_type": "string",
            "default_order": "asc",
        },
        SortBy.POKEMON_WIN_RATE: {
            "name": SortBy.POKEMON_WIN_RATE.value,
            "description": "Sort builds by Pokémon win rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.POKEMON_PICK_RATE: {
            "name": SortBy.POKEMON_PICK_RATE.value,
            "description": "Sort builds by Pokémon pick rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.MOVESET_WIN_RATE: {
            "name": SortBy.MOVESET_WIN_RATE.value,
            "description": "Sort builds by moveset win rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.MOVESET_PICK_RATE: {
            "name": SortBy.MOVESET_PICK_RATE.value,
            "description": "Sort builds by moveset pick rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.MOVESET_TRUE_PICK_RATE: {
            "name": SortBy.MOVESET_TRUE_PICK_RATE.value,
            "description": "Sort builds by moveset true pick rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.ITEM: {
            "name": SortBy.ITEM.value,
            "description": "Sort builds by item name (alphabetically).",
            "field_type": "string",
            "default_order": "asc",
        },
        SortBy.MOVESET_ITEM_WIN_RATE: {
            "name": SortBy.MOVESET_ITEM_WIN_RATE.value,
            "description": "Sort builds by moveset item win rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.MOVESET_ITEM_PICK_RATE: {
            "name": SortBy.MOVESET_ITEM_PICK_RATE.value,
            "description": "Sort builds by moveset item pick rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
        SortBy.MOVESET_ITEM_TRUE_PICK_RATE: {
            "name": SortBy.MOVESET_ITEM_TRUE_PICK_RATE.value,
            "description": "Sort builds by moveset item true pick rate (percentage).",
            "field_type": "float",
            "default_order": "desc",
        },
    }

    return criteria_info[sort_by_enum]


# /ids endpoint
@app.get(
    "/ids",
    response_model=List[int],
    summary="Get list of all build IDs",
    description="Returns a list of all build IDs in the database.",
)
def get_ids():
    """Get list of all build IDs"""
    LOG.info("get_ids")
    with BuildRepository() as repo:
        builds = repo.get_all_builds()
    return [build.id for build in builds]


# /filters endpoints
@app.get(
    "/filters",
    response_model=List[dict],
    summary="Get list of available filter strategies",
    description="Returns a list of all available filter strategies for builds.",
)
def get_filters():
    """Get list of available filter strategies"""
    LOG.info("get_filters")
    return [
        {
            "name": "pokemon",
            "description": "Filter builds by Pokémon name(s). Accepts comma-separated list.",
            "type": "include",
            "example": "pikachu,charizard",
        },
        {
            "name": "role",
            "description": "Filter builds by role(s). Accepts comma-separated list.",
            "type": "include",
            "example": "attacker,defender",
        },
        {
            "name": "item",
            "description": "Filter builds by item(s). Accepts comma-separated list.",
            "type": "include",
            "example": "potion,ejectbutton",
        },
        {
            "name": "ignore_pokemon",
            "description": "Exclude builds with specific Pokémon name(s). Accepts comma-separated list.",
            "type": "exclude",
            "example": "pikachu,charizard",
        },
        {
            "name": "ignore_role",
            "description": "Exclude builds with specific role(s). Accepts comma-separated list.",
            "type": "exclude",
            "example": "attacker,defender",
        },
        {
            "name": "ignore_item",
            "description": "Exclude builds with specific item(s). Accepts comma-separated list.",
            "type": "exclude",
            "example": "potion,ejectbutton",
        },
    ]


@app.get(
    "/filters/{filter_name}",
    response_model=dict,
    summary="Get details about a specific filter",
    description="Returns detailed information about the specified filter strategy.",
)
def get_filter_details(
    filter_name: str = Path(..., description="Filter strategy name"),
):
    """Get details about a specific filter strategy"""
    LOG.info("get_filter_details")
    LOG.debug("filter_name: %s", filter_name)

    # Validate filter
    if filter_name not in FILTER_STRATEGIES:
        raise HTTPException(
            status_code=404,
            detail=f"Filter '{filter_name}' not found.",
        )

    filter_info = {
        "pokemon": {
            "name": "pokemon",
            "description": "Filter builds by Pokémon name(s).",
            "type": "include",
            "parameter": "pokemon",
            "value_format": "comma-separated string",
            "example": "pikachu,charizard,greninja",
            "usage": "Use this filter to include only builds for specific Pokémon. Multiple Pokémon can be specified separated by commas.",
        },
        "role": {
            "name": "role",
            "description": "Filter builds by role(s).",
            "type": "include",
            "parameter": "role",
            "value_format": "comma-separated string",
            "example": "attacker,defender",
            "usage": "Use this filter to include only builds for specific roles. Multiple roles can be specified separated by commas.",
            "available_values": [
                "All-Rounder",
                "Attacker",
                "Defender",
                "Supporter",
                "Speedster",
            ],
        },
        "item": {
            "name": "item",
            "description": "Filter builds by item(s).",
            "type": "include",
            "parameter": "item",
            "value_format": "comma-separated string",
            "example": "potion,ejectbutton",
            "usage": "Use this filter to include only builds with specific items. Multiple items can be specified separated by commas.",
        },
        "ignore_pokemon": {
            "name": "ignore_pokemon",
            "description": "Exclude builds with specific Pokémon name(s).",
            "type": "exclude",
            "parameter": "ignore_pokemon",
            "value_format": "comma-separated string",
            "example": "pikachu,charizard",
            "usage": "Use this filter to exclude builds for specific Pokémon. Multiple Pokémon can be specified separated by commas.",
        },
        "ignore_role": {
            "name": "ignore_role",
            "description": "Exclude builds with specific role(s).",
            "type": "exclude",
            "parameter": "ignore_role",
            "value_format": "comma-separated string",
            "example": "attacker,defender",
            "usage": "Use this filter to exclude builds for specific roles. Multiple roles can be specified separated by commas.",
            "available_values": [
                "All-Rounder",
                "Attacker",
                "Defender",
                "Supporter",
                "Speedster",
            ],
        },
        "ignore_item": {
            "name": "ignore_item",
            "description": "Exclude builds with specific item(s).",
            "type": "exclude",
            "parameter": "ignore_item",
            "value_format": "comma-separated string",
            "example": "potion,ejectbutton",
            "usage": "Use this filter to exclude builds with specific items. Multiple items can be specified separated by commas.",
        },
    }

    return filter_info[filter_name]


# /logs endpoint
@app.get(
    "/logs",
    response_model=dict,
    summary="Get API logs summary",
    description="Returns a summary of API logs and log files available.",
)
def get_logs():
    """Get API logs summary"""
    LOG.info("get_logs")

    import glob
    import os
    from pathlib import Path

    # Get log files from the project root
    project_root = Path(__file__).parent.parent.parent
    log_files = glob.glob(str(project_root / "log_*.log"))

    log_info = {
        "available_logs": [],
        "description": "API logging information",
        "note": "Log files are stored in the project root directory",
    }

    for log_file in sorted(log_files):
        log_name = os.path.basename(log_file)
        try:
            file_size = os.path.getsize(log_file)
            # Read last few lines
            with open(log_file, "r") as f:
                lines = f.readlines()
                last_lines = lines[-5:] if len(lines) >= 5 else lines

            log_info["available_logs"].append(
                {
                    "name": log_name,
                    "path": log_file,
                    "size_bytes": file_size,
                    "last_entries": [line.strip() for line in last_lines],
                }
            )
        except Exception as e:
            log_info["available_logs"].append(
                {
                    "name": log_name,
                    "path": log_file,
                    "error": f"Could not read log file: {str(e)}",
                }
            )

    return log_info
