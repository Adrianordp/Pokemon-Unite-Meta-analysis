from typing import List, Optional

from fastapi import FastAPI, Query

from api.build_response import BuildResponse
from repository.build_repository import BuildRepository
from util.log import setup_custom_logger

from .config import settings

LOG = setup_custom_logger("log_api")


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
    relevance: Optional[str] = Query("percentage_cutoff"),
    relevance_threshold: Optional[float] = Query(None),
    sort_by: Optional[str] = Query("moveset_item_win_rate"),
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
    builds = repo.get_all_builds_by_table(repo.table_name)

    # Filtering logic
    if id is not None:
        b = builds[id]
        return [BuildResponse(**b.__dict__)]

    if pokemon:
        pokemon_list = [p.strip().lower() for p in pokemon.split(",")]
        builds = [b for b in builds if b.pokemon.lower() in pokemon_list]

    if role:
        role_list = [r.strip().lower() for r in role.split(",")]
        builds = [b for b in builds if b.role.lower() in role_list]

    if item:
        item_list = [i.strip().lower() for i in item.split(",")]
        builds = [b for b in builds if b.item.lower() in item_list]

    if ignore_pokemon:
        ignore_pokemon_list = [
            p.strip().lower() for p in ignore_pokemon.split(",")
        ]
        builds = [
            b for b in builds if b.pokemon.lower() not in ignore_pokemon_list
        ]

    if ignore_item:
        ignore_item_list = [i.strip().lower() for i in ignore_item.split(",")]
        builds = [b for b in builds if b.item.lower() not in ignore_item_list]

    if ignore_role:
        ignore_role_list = [r.strip().lower() for r in ignore_role.split(",")]
        builds = [b for b in builds if b.role.lower() not in ignore_role_list]

    if relevance == "percentage_cutoff" and relevance_threshold is None:
        LOG.warning(
            "Relevance is 'percentage_cutoff' but no relevance_threshold provided. Using default of 2.0."
        )
        relevance_threshold = 2.0  # Default threshold for percentage_cutoff

    # Relevance threshold filtering
    if relevance_threshold is not None:
        LOG.debug("Applying relevance threshold filtering")

        if relevance == "percentage_cutoff":
            LOG.debug("Applying percentage_cutoff filtering")
            builds = [
                b
                for b in builds
                if b.moveset_item_true_pick_rate >= relevance_threshold
            ]
        # Add more relevance strategies as needed

    # Sorting
    reverse = sort_order == "desc"
    if sort_by == "win_rate":
        builds = sorted(
            builds, key=lambda b: b.pokemon_win_rate, reverse=reverse
        )
    elif sort_by == "moveset_win_rate":
        builds = sorted(
            builds, key=lambda b: b.moveset_win_rate, reverse=reverse
        )
    elif sort_by == "moveset_item_win_rate":
        builds = sorted(
            builds, key=lambda b: b.moveset_item_win_rate, reverse=reverse
        )
    elif sort_by == "usage":
        builds = sorted(
            builds, key=lambda b: b.pokemon_pick_rate, reverse=reverse
        )
    elif sort_by == "relevance":
        builds = sorted(
            builds, key=lambda b: b.moveset_true_pick_rate, reverse=reverse
        )

    # Convert to response model
    return [BuildResponse(**b.__dict__) for b in builds]
