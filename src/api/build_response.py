"""
Pydantic response model for Build
"""

from pydantic import BaseModel


# Pydantic response model for Build
class BuildResponse(BaseModel):
    """
    Pydantic response model for Build
    """

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
