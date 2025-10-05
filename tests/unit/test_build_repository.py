import sqlite3

from conftest import create_build_response

from repository.build_repository import BuildRepository


def test_create_and_retrieve_build(build_repository, sample_week):
    # Arrange
    build = create_build_response(
        id=0,
        week=sample_week,
        pokemon="Charizard",
        role="All-Rounder",
        pokemon_win_rate=0.51,
        pokemon_pick_rate=0.18,
        move_1="Flamethrower",
        move_2="Fire Blast",
        moveset_win_rate=0.53,
        moveset_pick_rate=0.14,
        moveset_true_pick_rate=0.09,
        item="XSpeed",
        moveset_item_win_rate=0.54,
        moveset_item_pick_rate=0.11,
        moveset_item_true_pick_rate=0.07,
    )

    # Act
    build_repository.create(build, week=sample_week)
    builds = build_repository.get_all_builds(week=sample_week)

    # Assert
    assert len(builds) == 1
    assert builds[0].pokemon == "Charizard"
    assert builds[0].role == "All-Rounder"
    assert builds[0].week == sample_week


def test_set_table_name():
    # Arrange
    repo = BuildRepository()

    # Act
    repo.set_table_name("my_table")

    # Assert
    assert repo.table_name == "my_table"


def test_get_table_names_returns_empty_on_error():
    # Arrange
    repo = BuildRepository(conn=sqlite3.connect(":memory:"))

    # No sqlite_sequence table in a fresh in-memory DB
    # Act & Assert
    assert repo.get_table_names() == []


def test_get_table_names_with_tables():
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create a table and insert a row to ensure sqlite_sequence exists
    cursor.execute(
        "CREATE TABLE test_table (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"
    )
    cursor.execute("INSERT INTO test_table (name) VALUES ('foo')")
    conn.commit()
    repo = BuildRepository(conn=conn)

    # Now sqlite_sequence should exist and contain 'test_table'
    # Act
    table_names = repo.get_table_names()

    # Assert
    assert "test_table" in table_names


def test_commit_does_not_raise():
    # Arrange & Act
    repo = BuildRepository(conn=sqlite3.connect(":memory:"))
    # Should not raise
    repo.commit()

    # Assert - nothing to assert, just ensuring no exception


def test_create_returns_false_if_table_doesnt_exist(sample_week):
    # Arrange: Create repository with empty in-memory database
    conn = sqlite3.connect(":memory:")
    repo = BuildRepository(conn=conn)
    build = create_build_response(
        id=0,
        week=sample_week,
        pokemon="Pikachu",
        role="Attacker",
        pokemon_win_rate=0.5,
        pokemon_pick_rate=0.2,
        move_1="Thunderbolt",
        move_2="Volt Tackle",
        moveset_win_rate=0.51,
        moveset_pick_rate=0.15,
        moveset_true_pick_rate=0.1,
        item="Purify",
        moveset_item_win_rate=0.52,
        moveset_item_pick_rate=0.12,
        moveset_item_true_pick_rate=0.08,
    )

    # Act & Assert: Should return False because table doesn't exist
    assert repo.create(build, week=sample_week) is False


def test_get_all_pokemons_by_table(build_repository, sample_week):
    # Arrange
    build = create_build_response(
        id=0,
        week=sample_week,
        pokemon="Snorlax",
        role="Defender",
        pokemon_win_rate=0.6,
        pokemon_pick_rate=0.25,
        move_1="Tackle",
        move_2="Block",
        moveset_win_rate=0.61,
        moveset_pick_rate=0.2,
        moveset_true_pick_rate=0.13,
        item="ShedinjaDoll",
        moveset_item_win_rate=0.62,
        moveset_item_pick_rate=0.18,
        moveset_item_true_pick_rate=0.1,
    )

    # Act
    build_repository.create(build, week=sample_week)
    pokemons = build_repository.get_all_pokemons_by_table("builds")

    # Assert
    assert "Snorlax" in pokemons


def test_create_operational_error(sample_week):
    # Arrange: Use an invalid table name to trigger sqlite3.OperationalError
    conn = sqlite3.connect(":memory:")
    repo = BuildRepository(conn=conn)
    repo.table_name = "invalid table name!"  # Invalid table name

    build = create_build_response(
        id=0,
        week=sample_week,
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

    # Act
    result = repo.create(build, week=sample_week)

    # Assert
    assert result is False


def test_get_available_weeks(build_repository, sample_week):
    # Arrange
    build1 = create_build_response(id=0, week=sample_week, pokemon="Pikachu")
    build2 = create_build_response(id=0, week="Y2025m10d05", pokemon="Snorlax")

    # Act
    build_repository.create(build1, week=sample_week)
    build_repository.create(build2, week="Y2025m10d05")
    weeks = build_repository.get_available_weeks()

    # Assert
    assert sample_week in weeks
    assert "Y2025m10d05" in weeks
    assert len(weeks) == 2
