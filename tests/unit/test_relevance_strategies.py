from entity.build import Build
from pokemon_unite_meta_analysis.relevance_strategy import (
    relevance_any,
    relevance_moveset_item_true_pr,
    relevance_position_of_popularity,
)


def make_builds():
    return [
        Build(
            pokemon="Snorlax",
            role="Defender",
            pokemon_win_rate=0.60,
            pokemon_pick_rate=0.25,
            move_1="Tackle",
            move_2="Block",
            moveset_win_rate=0.62,
            moveset_pick_rate=0.20,
            moveset_true_pick_rate=0.15,
            item="Leftovers",
            moveset_item_win_rate=0.63,
            moveset_item_pick_rate=0.18,
            moveset_item_true_pick_rate=0.12,
        ),
        Build(
            pokemon="Gengar",
            role="Speedster",
            pokemon_win_rate=0.58,
            pokemon_pick_rate=0.22,
            move_1="Shadow Ball",
            move_2="Sludge Bomb",
            moveset_win_rate=0.59,
            moveset_pick_rate=0.19,
            moveset_true_pick_rate=0.13,
            item="Choice Specs",
            moveset_item_win_rate=0.60,
            moveset_item_pick_rate=0.16,
            moveset_item_true_pick_rate=0.10,
        ),
    ]

def test_relevance_any():
    builds = make_builds()
    result = relevance_any(builds, threshold=0.0, get_builds=lambda: builds)
    assert result == builds

def test_relevance_moveset_item_true_pr():
    builds = make_builds()
    result = relevance_moveset_item_true_pr(builds, threshold=0.11, get_builds=lambda: builds)
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"

def test_relevance_position_of_popularity():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = relevance_position_of_popularity(builds, threshold=1, get_builds=lambda: builds)
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"
