from typing import List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from repository.build_repository import BuildRepository
from util.log import setup_custom_logger

from .config import settings

LOG = setup_custom_logger("api")


# Pydantic response model for Build
class BuildResponse(BaseModel):
    pokemon: str
    role: str
    pokemon_win_rate: float
    pokemon_pick_rate: float
    move_1: str
    move_2: str
    moveset_win_rate: float
    moveset_pick_rate: float
    moveset_true_pick_rate: float
    item: str
    moveset_item_win_rate: float
    moveset_item_pick_rate: float
    moveset_item_true_pick_rate: float


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
    relevance: Optional[str] = Query("win_rate"),
    relevance_threshold: Optional[float] = Query(None),
    sort_by: Optional[str] = Query("win_rate"),
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
        builds = [b for b in builds if getattr(b, "id", None) == id]
    if pokemon:
        pokemon_list = [p.strip() for p in pokemon.split(",")]
        builds = [b for b in builds if b.pokemon in pokemon_list]
    if role:
        role_list = [r.strip() for r in role.split(",")]
        builds = [b for b in builds if b.role in role_list]
    if item:
        item_list = [i.strip() for i in item.split(",")]
        builds = [b for b in builds if b.item in item_list]
    if ignore_pokemon:
        ignore_pokemon_list = [p.strip() for p in ignore_pokemon.split(",")]
        builds = [b for b in builds if b.pokemon not in ignore_pokemon_list]
    if ignore_item:
        ignore_item_list = [i.strip() for i in ignore_item.split(",")]
        builds = [b for b in builds if b.item not in ignore_item_list]
    if ignore_role:
        ignore_role_list = [r.strip() for r in ignore_role.split(",")]
        builds = [b for b in builds if b.role not in ignore_role_list]

    # Relevance threshold filtering
    if relevance_threshold is not None:
        if relevance == "win_rate":
            builds = [
                b for b in builds if b.pokemon_win_rate >= relevance_threshold
            ]
        # Add more relevance strategies as needed

    # Sorting
    reverse = sort_order == "desc"
    if sort_by == "win_rate":
        builds = sorted(
            builds, key=lambda b: b.pokemon_win_rate, reverse=reverse
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
