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
