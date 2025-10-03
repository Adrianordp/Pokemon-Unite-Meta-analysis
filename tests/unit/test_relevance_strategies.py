from conftest import create_build_response

from pokemon_unite_meta_analysis.relevance_strategy import (
    RELEVANCE_STRATEGIES,
    RelevanceStrategy,
)


def make_builds():
    """Helper function to create test builds with id and week"""
    week = "Y2025m09d28"
    return [
        create_build_response(
            id=1,
            week=week,
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
        create_build_response(
            id=2,
            week=week,
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
        create_build_response(
            id=3,
            week=week,
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
        create_build_response(
            id=4,
            week=week,
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


class DummyRelevanceStrategy(RelevanceStrategy):
    pass


def test_relevance_not_implemented():
    # Arrange
    strategy = DummyRelevanceStrategy()

    try:
        # Act
        strategy.apply([], 0.0, lambda: [])

        # Assert
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass  # Expected exception


def test_relevance_any():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["any"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )

    # Assert
    assert result == builds


def test_relevance_percentage():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=11, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_percentage_no_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_percentage_high_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=101, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 0


def test_relevance_percentage_zero_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["percentage"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_invalid():
    # Arrange
    builds = make_builds()
    try:
        # Act
        RELEVANCE_STRATEGIES["invalid"].apply(
            builds, threshold=1, get_builds=lambda: builds
        )
        # Assert
        assert False, "Expected KeyError for invalid relevance strategy"
    except KeyError:
        pass  # Expected exception


def test_relevance_top_n():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_top_n_no_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_top_n_zero_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 0


def test_relevance_top_n_high_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["top_n"].apply(
        builds, threshold=10, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_cumulative_coverage():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=12, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_cumulative_coverage_no_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_cumulative_coverage_zero_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 0


def test_relevance_cumulative_coverage_high_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["cumulative_coverage"].apply(
        builds, threshold=101, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_quartile():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 1
    assert result[0].pokemon == "Snorlax"


def test_relevance_quartile_no_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=None, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_quartile_zero_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=0, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 0


def test_relevance_quartile_zero_sized_builds():
    # Arrange
    builds = []

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 0


def test_relevance_quartile_threshold_2():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=2, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 2
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"


def test_relevance_quartile_threshold_3():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=3, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 3
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"


def test_relevance_quartile_threshold_4():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=4, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 4
    assert result[0].pokemon == "Snorlax"
    assert result[1].pokemon == "Gengar"
    assert result[2].pokemon == "Pikachu"
    assert result[3].pokemon == "Lucario"


def test_relevance_quartile_invalid_threshold():
    # Arrange
    builds = make_builds()

    # Act
    result = RELEVANCE_STRATEGIES["quartile"].apply(
        builds, threshold=1.5, get_builds=lambda: builds
    )

    # Assert
    assert len(result) == 0
