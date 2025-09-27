"""
Defines relevance criteria for filtering builds based on different strategies.
"""


from enum import Enum


class Relevance(Enum):
    """
    Relevance enum class
    """

    ANY = "any"
    MOVESET_ITEM_TRUE_PR = "moveset_item_true_pr"
    POSITION_OF_POPULARITY = "position_of_popularity"