import sqlite3

from entity.build import Build
from repository.build_repository import BuildRepository


def test_create_and_retrieve_build():
    # Arrange: Set up the in-memory SQLite DB for isolation
    repo = BuildRepository(
        table_name="test_table", conn=sqlite3.connect(":memory:")
    )
    build = Build(
        pokemon="Charizard",
        role="All-Rounder",
        pokemon_win_rate=0.51,
        pokemon_pick_rate=0.18,
        move_1="Flamethrower",
        move_2="Fire Blast",
        moveset_win_rate=0.53,
        moveset_pick_rate=0.14,
        moveset_true_pick_rate=0.09,
        item="Muscle Band",
        moveset_item_win_rate=0.54,
        moveset_item_pick_rate=0.11,
        moveset_item_true_pick_rate=0.07,
    )

    # Act: Create a build and retrieve it
    repo._create_table()
    repo.create(build)
    builds = repo.get_all_builds_by_table("test_table")

    # Assert: Verify the build was created and retrieved correctly
    assert len(builds) == 1
    assert builds[0].pokemon == "Charizard"
    assert builds[0].role == "All-Rounder"
