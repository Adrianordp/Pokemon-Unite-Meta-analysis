"""
Build class for pokemon builds

This class definition creates a dataclass named Build to represent Pokémon
builds.

pokemon:
    The name of the Pokémon.
role:
    The role of the Pokémon.
pokemon_win_rate and pokemon_pick_rate:
    The win rate and pick rate of the Pokémon, respectively.
move_1 and move_2:
    The two moves of the Pokémon.
moveset_win_rate and moveset_pick_rate:
    The win rate and pick rate of the moveset, respectively.
moveset_true_pick_rate:
    The true pick rate of the moveset.
item:
    The item used by the Pokémon.
moveset_item_win_rate and moveset_item_pick_rate:
    The win rate and pick rate of the moveset with the item, respectively.
moveset_item_true_pick_rate:
    The true pick rate of the moveset with the item.

Note that this class does not have any methods, only attributes. The @dataclass
decorator automatically generates special methods like init, __repr__, and
__eq__ for the class.
"""

from dataclasses import dataclass


@dataclass
class Build:
    """
    Dataclass for pokemon builds
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
