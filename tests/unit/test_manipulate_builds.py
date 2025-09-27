from unittest.mock import MagicMock

from entity.build import Build
from pokemon_unite_meta_analysis.manipulate_builds import (
    ManipulateBuilds,
    Relevance,
    SortBy,
)


def test_manipulate_builds_sort_and_json():
    # Arrange
    mock_repo = MagicMock()
    mock_repo.get_all_builds_by_table.return_value = [
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

    # Act
    manip = ManipulateBuilds(mock_repo, "dummy_date")
    result_json = manip.run(
        sort_by=SortBy.POKEMON_WIN_RATE,
        top_n=1,
        relevance=Relevance.ANY,
        print_result=False,
    )

    # Assert
    assert "Snorlax" in result_json
    assert "Gengar" not in result_json


def test_manipulate_builds_moveset_item_true_pr():
    mock_repo = MagicMock()
    builds = [
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
    mock_repo.get_all_builds_by_table.return_value = builds
    manip = ManipulateBuilds(mock_repo, "dummy_date")
    result_json = manip.run(
        sort_by=SortBy.POKEMON_WIN_RATE,
        top_n=2,
        relevance=Relevance.MOVESET_ITEM_TRUE_PR,
        relevance_threshold=0.11,
        print_result=False,
    )
    assert "Snorlax" in result_json
    assert "Gengar" not in result_json


def test_manipulate_builds_position_of_popularity():
    mock_repo = MagicMock()
    builds = [
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
    mock_repo.get_all_builds_by_table.return_value = builds
    manip = ManipulateBuilds(mock_repo, "dummy_date")
    # Should select the most popular (highest moveset_item_true_pick_rate)
    result_json = manip.run(
        sort_by=SortBy.POKEMON_WIN_RATE,
        top_n=2,
        relevance=Relevance.POSITION_OF_POPULARITY,
        relevance_threshold=1,
        print_result=False,
    )
    assert "Snorlax" in result_json
    assert "Gengar" not in result_json


def test_manipulate_builds_unsupported_relevance():
    mock_repo = MagicMock()
    mock_repo.get_all_builds_by_table.return_value = []
    manip = ManipulateBuilds(mock_repo, "dummy_date")
    class FakeRelevance:
        pass
    try:
        manip.run(
            sort_by=SortBy.POKEMON_WIN_RATE,
            relevance=FakeRelevance(),
        )
    except ValueError as e:
        assert "not supported" in str(e)
    else:
        assert False, "ValueError not raised"


def test_head_returns_n_builds():
    mock_repo = MagicMock()
    builds = [
        Build(
            pokemon=f"Poke{i}",
            role="Role",
            pokemon_win_rate=0.5,
            pokemon_pick_rate=0.2,
            move_1="Move1",
            move_2="Move2",
            moveset_win_rate=0.51,
            moveset_pick_rate=0.15,
            moveset_true_pick_rate=0.1,
            item="Item",
            moveset_item_win_rate=0.52,
            moveset_item_pick_rate=0.12,
            moveset_item_true_pick_rate=0.08,
        ) for i in range(5)
    ]
    manip = ManipulateBuilds(mock_repo, "dummy_date")
    result = manip._head(builds, n=3)
    assert len(result) == 3


def test_head_returns_all_builds():
    mock_repo = MagicMock()
    builds = [
        Build(
            pokemon=f"Poke{i}",
            role="Role",
            pokemon_win_rate=0.5,
            pokemon_pick_rate=0.2,
            move_1="Move1",
            move_2="Move2",
            moveset_win_rate=0.51,
            moveset_pick_rate=0.15,
            moveset_true_pick_rate=0.1,
            item="Item",
            moveset_item_win_rate=0.52,
            moveset_item_pick_rate=0.12,
            moveset_item_true_pick_rate=0.08,
        ) for i in range(5)
    ]
    manip = ManipulateBuilds(mock_repo, "dummy_date")
    result = manip._head(builds)
    assert len(result) == 5
