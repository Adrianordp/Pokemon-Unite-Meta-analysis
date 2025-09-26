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

def test_set_table_name():
    repo = BuildRepository()
    repo.set_table_name("my_table")
    assert repo.table_name == "my_table"

def test_get_table_names_returns_empty_on_error():
    repo = BuildRepository(conn=sqlite3.connect(":memory:"))
    # No sqlite_sequence table in a fresh in-memory DB
    assert repo.get_table_names() == []


def test_get_table_names_with_tables():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create a table and insert a row to ensure sqlite_sequence exists
    cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cursor.execute("INSERT INTO test_table (name) VALUES ('foo')")
    conn.commit()
    repo = BuildRepository(conn=conn)
    # Now sqlite_sequence should exist and contain 'test_table'
    table_names = repo.get_table_names()
    assert "test_table" in table_names

def test_commit_does_not_raise():
    repo = BuildRepository(conn=sqlite3.connect(":memory:"))
    # Should not raise
    repo.commit()

def test_create_returns_false_if_table_name_not_set():
    repo = BuildRepository(table_name=None, conn=sqlite3.connect(":memory:"))
    build = Build(
        pokemon="Pikachu",
        role="Attacker",
        pokemon_win_rate=0.5,
        pokemon_pick_rate=0.2,
        move_1="Thunderbolt",
        move_2="Volt Tackle",
        moveset_win_rate=0.51,
        moveset_pick_rate=0.15,
        moveset_true_pick_rate=0.1,
        item="Wise Glasses",
        moveset_item_win_rate=0.52,
        moveset_item_pick_rate=0.12,
        moveset_item_true_pick_rate=0.08,
    )
    # Should print error and return False
    assert repo.create(build) is False

def test_get_all_pokemons_by_table():
    repo = BuildRepository(table_name="poke_table", conn=sqlite3.connect(":memory:"))
    repo._create_table()
    build = Build(
        pokemon="Snorlax",
        role="Defender",
        pokemon_win_rate=0.6,
        pokemon_pick_rate=0.25,
        move_1="Tackle",
        move_2="Block",
        moveset_win_rate=0.61,
        moveset_pick_rate=0.2,
        moveset_true_pick_rate=0.13,
        item="Leftovers",
        moveset_item_win_rate=0.62,
        moveset_item_pick_rate=0.18,
        moveset_item_true_pick_rate=0.1,
    )
    repo.create(build)
    pokemons = repo.get_all_pokemons_by_table("poke_table")
    assert pokemons == ["Snorlax"]


def test_create_operational_error():
    # Use an invalid table name to trigger sqlite3.OperationalError
    repo = BuildRepository(table_name="invalid table name!", conn=sqlite3.connect(":memory:"))
    build = Build(
        pokemon="Bulbasaur",
        role="Supporter",
        pokemon_win_rate=0.4,
        pokemon_pick_rate=0.1,
        move_1="Vine Whip",
        move_2="Razor Leaf",
        moveset_win_rate=0.41,
        moveset_pick_rate=0.09,
        moveset_true_pick_rate=0.05,
        item="Shell Bell",
        moveset_item_win_rate=0.42,
        moveset_item_pick_rate=0.07,
        moveset_item_true_pick_rate=0.03,
    )
    result = repo.create(build)
    assert result is False
