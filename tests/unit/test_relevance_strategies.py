from entity.build_response import BuildResponse
from pokemon_unite_meta_analysis.relevance_strategy import RELEVANCE_STRATEGIES


def make_builds():
    return [
        BuildResponse(
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
        BuildResponse(
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
    result = RELEVANCE_STRATEGIES["any"].apply(
        builds, threshold=0.0, get_builds=lambda: builds
    )
    assert result == builds


def test_relevance_percentage():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=0.11, get_builds=lambda: builds
    )
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_quartile():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )
    assert len(result) == 0


def test_relevance_quartile_no_threshold():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )
    assert len(result) == 2
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"


def test_relevance_invalid():
    builds = make_builds()
    try:
        RELEVANCE_STRATEGIES["invalid"].apply(
            builds, threshold=0.1, get_builds=lambda: builds
        )
        assert False, "Expected KeyError for invalid relevance strategy"
    except KeyError:
        pass  # Expected exception


def test_relevance_top_n():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_cumulative_coverage():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=0.11, get_builds=lambda: builds
    )
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"
