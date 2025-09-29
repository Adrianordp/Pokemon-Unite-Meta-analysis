from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from api.custom_log import LOG
from entity.build_response import BuildResponse
from pokemon_unite_meta_analysis.filter_strategy import FILTER_STRATEGIES
from pokemon_unite_meta_analysis.relevance_strategy import (
    RELEVANCE_STRATEGIES,
    Relevance,
)
from pokemon_unite_meta_analysis.sort_strategy import SORT_STRATEGIES, SortBy
from repository.build_repository import BuildRepository

from .config import settings

app = FastAPI(title=settings.api_name, debug=settings.debug)


@app.get("/")
def read_root():
    LOG.info("read_root")
    return {
        "message": f"{settings.api_name} is running.",
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
    }


# Health check endpoint
@app.get("/health")
def health_check():
    LOG.info("health_check")
    return {"status": "ok"}


# /builds endpoint with improved validation and error handling
@app.get(
    "/builds",
    response_model=List[BuildResponse],
    summary="Retrieve builds with filtering, sorting, and relevance options",
)
def get_builds(
    week: Optional[int] = Query(
        None, description="Week number for filtering builds"
    ),
    id: Optional[int] = Query(None, description="Build ID for direct lookup"),
    relevance: Optional[str] = Query(
        Relevance.ANY.value,
        description="Relevance strategy (any, moveset_item_true_pr, position_of_popularity)",
    ),
    relevance_threshold: Optional[float] = Query(
        0.0, description="Threshold for relevance filtering"
    ),
    sort_by: Optional[str] = Query(
        SortBy.MOVESET_ITEM_TRUE_PICK_RATE.value, description="Field to sort by"
    ),
    sort_order: Optional[str] = Query(
        "desc", description="Sort order: asc or desc"
    ),
    pokemon: Optional[str] = Query(None, description="Filter by Pokémon name"),
    role: Optional[str] = Query(None, description="Filter by role"),
    item: Optional[str] = Query(None, description="Filter by item"),
    ignore_pokemon: Optional[str] = Query(
        None, description="Exclude Pokémon name"
    ),
    ignore_item: Optional[str] = Query(None, description="Exclude item"),
    ignore_role: Optional[str] = Query(None, description="Exclude role"),
    top_n: Optional[int] = Query(None, description="Limit to top N results"),
):
    LOG.info("get_builds")
    LOG.debug("week: %s", week)
    LOG.debug("id: %s", id)
    LOG.debug("relevance: %s", relevance)
    LOG.debug("relevance_threshold: %s", relevance_threshold)
    LOG.debug("sort_by: %s", sort_by)
    LOG.debug("sort_order: %s", sort_order)
    LOG.debug("pokemon: %s", pokemon)
    LOG.debug("role: %s", role)
    LOG.debug("item: %s", item)
    LOG.debug("ignore_pokemon: %s", ignore_pokemon)
    LOG.debug("ignore_item: %s", ignore_item)
    LOG.debug("ignore_role: %s", ignore_role)
    LOG.debug("top_n: %s", top_n)

    repo = BuildRepository()
    all_builds = repo.get_all_builds_by_table(repo.table_name)
    builds = all_builds.copy()

    # Direct ID lookup
    if id is not None:
        if id < 0 or id >= len(builds):
            raise HTTPException(status_code=404, detail="Build ID not found")
        b = builds[id]
        return [BuildResponse(**b.__dict__)]

    # Validate and map relevance
    try:
        relevance_enum = Relevance(relevance)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid relevance strategy: {relevance}"
        )

    # Apply relevance strategy
    builds = RELEVANCE_STRATEGIES[relevance_enum].apply(
        builds, relevance_threshold, lambda: all_builds
    )

    # Apply filter strategies
    if pokemon:
        builds = FILTER_STRATEGIES["pokemon"].apply(builds, pokemon)
    elif ignore_pokemon:
        builds = FILTER_STRATEGIES["ignore_pokemon"].apply(
            builds, ignore_pokemon
        )

    if role:
        builds = FILTER_STRATEGIES["role"].apply(builds, role)
    elif ignore_role:
        builds = FILTER_STRATEGIES["ignore_role"].apply(builds, ignore_role)

    if item:
        builds = FILTER_STRATEGIES["item"].apply(builds, item)
    elif ignore_item:
        builds = FILTER_STRATEGIES["ignore_item"].apply(builds, ignore_item)

    # Validate and map sort_by
    try:
        sort_by_enum = SortBy(sort_by)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid sort_by field: {sort_by}"
        )

    reverse = sort_order == "desc"
    builds = SORT_STRATEGIES[sort_by_enum.value].apply(builds, reverse=reverse)

    # Limit to top_n results if specified
    if top_n is not None and top_n > 0:
        builds = builds[:top_n]

    # Convert to response model
    return [BuildResponse(**b.__dict__) for b in builds]
