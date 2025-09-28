"""
Defines sorting criteria for builds based on different attributes.
"""

from enum import Enum


class SortBy(Enum):
    """
    SortBy enum class
    """

    POKEMON = "pokemon"
    ROLE = "role"
    POKEMON_WIN_RATE = "pokemon_win_rate"
    POKEMON_PICK_RATE = "pokemon_pick_rate"
    MOVE_1 = "move_1"
    MOVE_2 = "move_2"
    MOVESET_WIN_RATE = "moveset_win_rate"
    MOVESET_PICK_RATE = "moveset_pick_rate"
    MOVESET_TRUE_PICK_RATE = "moveset_true_pick_rate"
    ITEM = "item"
    MOVESET_ITEM_WIN_RATE = "moveset_item_win_rate"
    MOVESET_ITEM_PICK_RATE = "moveset_item_pick_rate"
    MOVESET_ITEM_TRUE_PICK_RATE = "moveset_item_true_pick_rate"
