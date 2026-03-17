"""
Pydantic model for Build database entity
"""

from pydantic import BaseModel


class BuildModel(BaseModel):
    """
    Pydantic model for Build database entity

    This model represents the structure of builds as stored in the database.

    Attributes:
        id: The unique identifier for the build.
        week: The week identifier for the build.
        pokemon: The name of the Pokémon.
        role: The role of the Pokémon.
        pokemon_win_rate: The win rate of the Pokémon.
        pokemon_pick_rate: The pick rate of the Pokémon.
        move_1: The first move of the Pokémon.
        move_2: The second move of the Pokémon.
        moveset_win_rate: The win rate of the moveset.
        moveset_pick_rate: The pick rate of the moveset.
        moveset_true_pick_rate: The true pick rate of the moveset.
        item: The item used by the Pokémon.
        moveset_item_win_rate: The win rate of the moveset with the item.
        moveset_item_pick_rate: The pick rate of the moveset with the item.
        moveset_item_true_pick_rate: The true pick rate of the moveset with
            the item.
    """

    id: int
    week: str
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
