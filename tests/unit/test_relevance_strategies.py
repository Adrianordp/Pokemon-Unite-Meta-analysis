from entity.build_response import BuildResponse
from pokemon_unite_meta_analysis.relevance_strategy import RELEVANCE_STRATEGIES


def make_builds():
    return [
        BuildResponse(
            pokemon="Snorlax",
            role="Defender",
            pokemon_win_rate=60,
            pokemon_pick_rate=25,
            move_1="Tackle",
            move_2="Block",
            moveset_win_rate=62,
            moveset_pick_rate=20,
            moveset_true_pick_rate=15,
            item="Leftovers",
            moveset_item_win_rate=63,
            moveset_item_pick_rate=18,
            moveset_item_true_pick_rate=12,
        ),
        BuildResponse(
            pokemon="Gengar",
            role="Speedster",
            pokemon_win_rate=58,
            pokemon_pick_rate=22,
            move_1="Shadow Ball",
            move_2="Sludge Bomb",
            moveset_win_rate=59,
            moveset_pick_rate=19,
            moveset_true_pick_rate=13,
            item="Choice Specs",
            moveset_item_win_rate=60,
            moveset_item_pick_rate=16,
            moveset_item_true_pick_rate=10,
        ),
        BuildResponse(
            pokemon="Pikachu",
            role="Attacker",
            pokemon_win_rate=55,
            pokemon_pick_rate=20,
            move_1="Thunderbolt",
            move_2="Quick Attack",
            moveset_win_rate=56,
            moveset_pick_rate=15,
            moveset_true_pick_rate=9,
            item="Electro Plate",
            moveset_item_win_rate=57,
            moveset_item_pick_rate=12,
            moveset_item_true_pick_rate=8,
        ),
        BuildResponse(
            pokemon="Lucario",
            role="All-Rounder",
            pokemon_win_rate=57,
            pokemon_pick_rate=18,
            move_1="Aura Sphere",
            move_2="Close Combat",
            moveset_win_rate=58,
            moveset_pick_rate=14,
            moveset_true_pick_rate=7,
            item="Muscle Band",
            moveset_item_win_rate=59,
            moveset_item_pick_rate=11,
            moveset_item_true_pick_rate=6,
        ),
    ]


def test_relevance_any():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["any"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )
    assert result == builds


def test_relevance_percentage():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=11, get_builds=lambda: builds
    )
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_percentage_no_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_percentage_high_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=101, get_builds=lambda: builds
    )
    assert len(result) == 0


def test_relevance_percentage_zero_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_invalid():
    builds = make_builds()
    try:
        RELEVANCE_STRATEGIES["invalid"].apply(
            builds, threshold=1, get_builds=lambda: builds
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


def test_relevance_top_n_no_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_top_n_zero_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )
    assert len(result) == 0


def test_relevance_top_n_high_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=10, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_cumulative_coverage():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=12, get_builds=lambda: builds
    )
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_cumulative_coverage_no_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_cumulative_coverage_zero_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )
    assert len(result) == 0


def test_relevance_cumulative_coverage_high_threshold():
    builds = make_builds()
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=101, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_quartile():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_quartile_no_threshold():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_quartile_zero_threshold():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )
    assert len(result) == 0


def test_relevance_quartile_zero_sized_builds():
    builds = []
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )
    assert len(result) == 0


def test_relevance_quartile_threshold_2():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=2, get_builds=lambda: builds
    )
    assert len(result) == 2
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"


def test_relevance_quartile_threshold_3():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=3, get_builds=lambda: builds
    )
    assert len(result) == 3
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"


def test_relevance_quartile_threshold_4():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=4, get_builds=lambda: builds
    )
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_quartile_invalid_threshold():
    builds = make_builds()
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1.5, get_builds=lambda: builds
    )
    assert len(result) == 0
