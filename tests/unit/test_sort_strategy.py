import pytest
from conftest import create_build_response

from pokemon_unite_meta_analysis.sort_strategy import (
    ItemSortStrategy,
    MovesetItemPickRateSortStrategy,
    MovesetItemTruePickRateSortStrategy,
    MovesetItemWinRateSortStrategy,
    MovesetPickRateSortStrategy,
    MovesetTruePickRateSortStrategy,
    MovesetWinRateSortStrategy,
    PokemonPickRateSortStrategy,
    PokemonSortStrategy,
    PokemonWinRateSortStrategy,
    RoleSortStrategy,
    SortStrategy,
)


class DummySortStrategy(SortStrategy):
    pass


@pytest.fixture
def sample_builds(sample_week):
    return [
        create_build_response(
            id=1,
            week=sample_week,
            pokemon="Pikachu",
            role="Attacker",
            pokemon_win_rate=55.0,
            pokemon_pick_rate=20.0,
            move_1="Thunderbolt",
            move_2="Volt Tackle",
            moveset_win_rate=52.0,
            moveset_pick_rate=18.0,
            moveset_true_pick_rate=17.0,
            item="Purify",
            moveset_item_win_rate=53.0,
            moveset_item_pick_rate=15.0,
            moveset_item_true_pick_rate=14.0,
        ),
        create_build_response(
            id=2,
            week=sample_week,
            pokemon="Snorlax",
            role="Defender",
            pokemon_win_rate=50.0,
            pokemon_pick_rate=15.0,
            move_1="Tackle",
            move_2="Block",
            moveset_win_rate=48.0,
            moveset_pick_rate=13.0,
            moveset_true_pick_rate=12.0,
            item="ShedinjaDoll",
            moveset_item_win_rate=49.0,
            moveset_item_pick_rate=10.0,
            moveset_item_true_pick_rate=9.0,
        ),
        create_build_response(
            id=3,
            week=sample_week,
            pokemon="Lucario",
            role="All-Rounder",
            pokemon_win_rate=60.0,
            pokemon_pick_rate=25.0,
            move_1="Power-Up Punch",
            move_2="Bone Rush",
            moveset_win_rate=58.0,
            moveset_pick_rate=22.0,
            moveset_true_pick_rate=21.0,
            item="XSpeed",
            moveset_item_win_rate=59.0,
            moveset_item_pick_rate=20.0,
            moveset_item_true_pick_rate=19.0,
        ),
    ]


def test_dummy_sort_strategy(sample_builds):
    # Arrange
    strategy = DummySortStrategy()

    # Act
    try:
        strategy.apply(sample_builds)
    except NotImplementedError:
        # Assert
        pass
    else:
        assert False, "NotImplementedError was not raised"


def test_pokemon_sort_strategy(sample_builds):
    # Arrange
    strategy = PokemonSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.pokemon for b in sorted_builds] == [
        "Lucario",
        "Pikachu",
        "Snorlax",
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=True)

    # Assert pt.2
    assert [b.pokemon for b in sorted_builds_rev] == [
        "Snorlax",
        "Pikachu",
        "Lucario",
    ]


def test_role_sort_strategy(sample_builds):
    # Arrange
    strategy = RoleSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.role for b in sorted_builds] == [
        "All-Rounder",
        "Attacker",
        "Defender",
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=True)

    # Assert pt.2
    assert [b.role for b in sorted_builds_rev] == [
        "Defender",
        "Attacker",
        "All-Rounder",
    ]


def test_pokemon_win_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = PokemonWinRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.pokemon_win_rate for b in sorted_builds] == [60.0, 55.0, 50.0]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.pokemon_win_rate for b in sorted_builds_rev] == [50.0, 55.0, 60.0]


def test_pokemon_pick_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = PokemonPickRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.pokemon_pick_rate for b in sorted_builds] == [25.0, 20.0, 15.0]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.pokemon_pick_rate for b in sorted_builds_rev] == [
        15.0,
        20.0,
        25.0,
    ]


def test_moveset_win_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = MovesetWinRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.moveset_win_rate for b in sorted_builds] == [58.0, 52.0, 48.0]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.moveset_win_rate for b in sorted_builds_rev] == [48.0, 52.0, 58.0]


def test_moveset_pick_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = MovesetPickRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.moveset_pick_rate for b in sorted_builds] == [22.0, 18.0, 13.0]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.moveset_pick_rate for b in sorted_builds_rev] == [
        13.0,
        18.0,
        22.0,
    ]


def test_moveset_true_pick_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = MovesetTruePickRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.moveset_true_pick_rate for b in sorted_builds] == [
        21.0,
        17.0,
        12.0,
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.moveset_true_pick_rate for b in sorted_builds_rev] == [
        12.0,
        17.0,
        21.0,
    ]


def test_item_sort_strategy(sample_builds):
    # Arrange
    strategy = ItemSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.item for b in sorted_builds] == [
        "Purify",
        "ShedinjaDoll",
        "XSpeed",
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=True)

    # Assert pt.2
    assert [b.item for b in sorted_builds_rev] == [
        "XSpeed",
        "ShedinjaDoll",
        "Purify",
    ]


def test_moveset_item_win_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = MovesetItemWinRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.moveset_item_win_rate for b in sorted_builds] == [
        59.0,
        53.0,
        49.0,
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.moveset_item_win_rate for b in sorted_builds_rev] == [
        49.0,
        53.0,
        59.0,
    ]


def test_moveset_item_pick_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = MovesetItemPickRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.moveset_item_pick_rate for b in sorted_builds] == [
        20.0,
        15.0,
        10.0,
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.moveset_item_pick_rate for b in sorted_builds_rev] == [
        10.0,
        15.0,
        20.0,
    ]


def test_moveset_item_true_pick_rate_sort_strategy(sample_builds):
    # Arrange
    strategy = MovesetItemTruePickRateSortStrategy()

    # Act pt.1
    sorted_builds = strategy.apply(sample_builds)

    # Assert pt.1
    assert [b.moveset_item_true_pick_rate for b in sorted_builds] == [
        19.0,
        14.0,
        9.0,
    ]

    # Act pt.2
    sorted_builds_rev = strategy.apply(sample_builds, reverse=False)

    # Assert pt.2
    assert [b.moveset_item_true_pick_rate for b in sorted_builds_rev] == [
        9.0,
        14.0,
        19.0,
    ]
