from typing import List

from fastapi import Depends, FastAPI, HTTPException, Path

from api.config import settings
from api.custom_log import LOG
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


# /pokemon endpoints
@app.get(
    "/pokemon",
    response_model=List[str],
    summary="Get list of available Pokémon",
    description="Returns a list of all unique Pokémon names in the builds database.",
)
def get_pokemon():
    repo = BuildRepository()
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
    repo = BuildRepository()
    builds = repo.get_all_builds()
    filtered = [
        build for build in builds if build.pokemon.lower() == name.lower()
    ]
    if not filtered:
        raise HTTPException(
            status_code=404, detail=f"Pokémon '{name}' not found."
        )
    return filtered


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
    repo = BuildRepository()
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

    repo = BuildRepository()

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
        return [builds[params.id]]

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

    # Convert to response model
    return [BuildResponse(**b.__dict__) for b in builds]
