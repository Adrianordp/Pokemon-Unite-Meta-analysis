"""
Enum for relevance strategies used in filtering Pokémon Unite builds.
"""

from enum import Enum


# Enum for relevance strategies
class Relevance(str, Enum):
    ANY = "any"
    PERCENTAGE = "percentage"
    TOP_N = "top_n"
    CUMULATIVE_COVERAGE = "cumulative_coverage"
    QUARTILE = "quartile"
