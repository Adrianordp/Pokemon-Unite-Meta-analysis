from typing import List, Optional

from fastapi import FastAPI, Query

from api.custom_log import LOG
from entity.build_response import BuildResponse
from pokemon_unite_meta_analysis.filter_strategy import FILTER_STRATEGIES
from pokemon_unite_meta_analysis.relevance_strategy import (
    RELEVANCE_STRATEGIES,
)
from pokemon_unite_meta_analysis.sort_strategy import SORT_STRATEGIES
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


# /builds endpoint with all query parameters
@app.get("/builds", response_model=List[BuildResponse])
def get_builds(
    week: Optional[int] = Query(None),
    id: Optional[int] = Query(None),
    relevance: Optional[str] = Query("percentage"),
    relevance_threshold: Optional[float] = Query(None),
    sort_by: Optional[str] = Query("moveset_item_true_pick_rate"),
    sort_order: Optional[str] = Query("desc"),
    pokemon: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    item: Optional[str] = Query(None),
    ignore_pokemon: Optional[str] = Query(None),
    ignore_item: Optional[str] = Query(None),
    ignore_role: Optional[str] = Query(None),
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

    repo = BuildRepository()
    all_builds = repo.get_all_builds_by_table(repo.table_name)
    builds = all_builds.copy()

    # Filtering logic using strategies
    if id is not None:
        b = builds[id]
        return [BuildResponse(**b.__dict__)]

    # Apply relevance strategy
    if relevance in RELEVANCE_STRATEGIES:
        builds = RELEVANCE_STRATEGIES[relevance].apply(
            builds, relevance_threshold, lambda: all_builds
        )
    else:
        LOG.error("Invalid relevance strategy: %s", relevance)

    # Apply filter strategies
    if pokemon:
        builds = FILTER_STRATEGIES["pokemon"].apply(builds, pokemon)

    if not pokemon and ignore_pokemon:
        builds = FILTER_STRATEGIES["ignore_pokemon"].apply(
            builds, ignore_pokemon
        )

    if role:
        builds = FILTER_STRATEGIES["role"].apply(builds, role)

    if not role and ignore_role:
        builds = FILTER_STRATEGIES["ignore_role"].apply(builds, ignore_role)

    if item:
        builds = FILTER_STRATEGIES["item"].apply(builds, item)

    if not item and ignore_item:
        builds = FILTER_STRATEGIES["ignore_item"].apply(builds, ignore_item)

    # Apply sorting strategy

    reverse = sort_order == "desc"
    if sort_by in SORT_STRATEGIES:
        builds = SORT_STRATEGIES[sort_by].apply(builds, reverse=reverse)
    else:
        LOG.error("Invalid sort_by strategy: %s", sort_by)

    # Convert to response model
    return [BuildResponse(**b.__dict__) for b in builds]
