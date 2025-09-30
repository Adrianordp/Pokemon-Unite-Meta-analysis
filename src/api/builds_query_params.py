from typing import Optional

from pydantic import BaseModel, Field

from pokemon_unite_meta_analysis.relevance_strategy import Relevance
from pokemon_unite_meta_analysis.sort_strategy import SortBy


class BuildsQueryParams(BaseModel):
    """
    Query parameters for the /builds endpoint.

    Attributes:
        week (Optional[int]): Week number for filtering builds.
        id (Optional[int]): Build ID for direct lookup.
        relevance (Optional[str]): Relevance strategy (any, moveset_item_true_pr, position_of_popularity).
        relevance_threshold (Optional[float]): Threshold for relevance filtering.
        sort_by (Optional[str]): Field to sort by.
        sort_order (Optional[str]): Sort order: asc or desc.
        pokemon (Optional[str]): Filter by Pokémon name.
        role (Optional[str]): Filter by role.
        item (Optional[str]): Filter by item.
        ignore_pokemon (Optional[str]): Exclude Pokémon name.
        ignore_item (Optional[str]): Exclude item.
        ignore_role (Optional[str]): Exclude role.
        top_n (Optional[int]): Limit to top N results.
    """

    week: Optional[int] = Field(
        None, description="Week number for filtering builds"
    )
    id: Optional[int] = Field(None, description="Build ID for direct lookup")
    relevance: Optional[str] = Field(
        Relevance.ANY.value,
        description="Relevance strategy (any, moveset_item_true_pr, position_of_popularity)",
    )
    relevance_threshold: Optional[float] = Field(
        0.0, description="Threshold for relevance filtering"
    )
    sort_by: Optional[str] = Field(
        SortBy.MOVESET_ITEM_TRUE_PICK_RATE.value, description="Field to sort by"
    )
    sort_order: Optional[str] = Field(
        "desc", description="Sort order: asc or desc"
    )
    pokemon: Optional[str] = Field(None, description="Filter by Pokémon name")
    role: Optional[str] = Field(None, description="Filter by role")
    item: Optional[str] = Field(None, description="Filter by item")
    ignore_pokemon: Optional[str] = Field(
        None, description="Exclude Pokémon name"
    )
    ignore_item: Optional[str] = Field(None, description="Exclude item")
    ignore_role: Optional[str] = Field(None, description="Exclude role")
    top_n: Optional[int] = Field(None, description="Limit to top N results")
