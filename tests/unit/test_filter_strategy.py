import pytest
from conftest import create_build_response

from pokemon_unite_meta_analysis.filter_strategy import (
    FilterStrategy,
    IgnoreItemFilterStrategy,
    IgnorePokemonFilterStrategy,
    IgnoreRoleFilterStrategy,
    ItemFilterStrategy,
    PokemonFilterStrategy,
    RoleFilterStrategy,
)


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


class DummyFilterStrategy(FilterStrategy):
    pass


def test_dummy_filter_strategy():
    # Arrange
    strategy = DummyFilterStrategy()
    try:
        # Act
        strategy.apply([], None)

        # Assert
        assert False, "Expected AttributeError for missing apply method"
    except NotImplementedError:
        pass  # Expected exception


def test_pokemon_filter_strategy(sample_builds):
    # Arrange
    strategy = PokemonFilterStrategy()

    # Act
    filtered = strategy.apply(sample_builds, "Pikachu, Lucario")

    # Assert
    assert len(filtered) == 2
    assert all(b.pokemon in ["Pikachu", "Lucario"] for b in filtered)


def test_role_filter_strategy(sample_builds):
    # Arrange
    strategy = RoleFilterStrategy()

    # Act
    filtered = strategy.apply(sample_builds, "Defender")

    # Assert
    assert len(filtered) == 1
    assert filtered[0].role == "Defender"


def test_item_filter_strategy(sample_builds):
    # Arrange
    strategy = ItemFilterStrategy()

    # Act
    filtered = strategy.apply(sample_builds, "Purify, XSpeed")

    # Assert
    assert len(filtered) == 2
    assert all(b.item in ["Purify", "XSpeed"] for b in filtered)


def test_ignore_pokemon_filter_strategy(sample_builds):
    # Arrange
    strategy = IgnorePokemonFilterStrategy()

    # Act
    filtered = strategy.apply(sample_builds, "Snorlax")

    # Assert
    assert len(filtered) == 2
    assert all(b.pokemon != "Snorlax" for b in filtered)


def test_ignore_role_filter_strategy(sample_builds):
    # Arrange
    strategy = IgnoreRoleFilterStrategy()

    # Act
    filtered = strategy.apply(sample_builds, "Attacker")

    # Assert
    assert len(filtered) == 2
    assert all(b.role != "Attacker" for b in filtered)


def test_ignore_item_filter_strategy(sample_builds):
    # Arrange
    strategy = IgnoreItemFilterStrategy()

    # Act
    filtered = strategy.apply(sample_builds, "ShedinjaDoll")

    # Assert
    assert len(filtered) == 2
    assert all(b.item != "ShedinjaDoll" for b in filtered)


def test_empty_value_returns_all(sample_builds):
    for strategy_cls in [
        PokemonFilterStrategy,
        RoleFilterStrategy,
        ItemFilterStrategy,
        IgnorePokemonFilterStrategy,
        IgnoreRoleFilterStrategy,
        IgnoreItemFilterStrategy,
    ]:
        # Arrange
        strategy = strategy_cls()

        # Act pt.1
        filtered = strategy.apply(sample_builds, None)

        # Assert pt.1
        assert filtered == sample_builds

        # Act pt.2
        filtered = strategy.apply(sample_builds, "")

        # Assert pt.2
        assert filtered == sample_builds
