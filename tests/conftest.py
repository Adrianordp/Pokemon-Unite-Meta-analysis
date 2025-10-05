"""
Test fixtures and utilities for Pokemon Unite Meta Analysis tests
"""

import sqlite3
from typing import List
from unittest.mock import MagicMock

import pytest

from entity.build_response import BuildResponse
from repository.build_repository import BuildRepository


@pytest.fixture
def sample_week() -> str:
    """Fixture providing a sample week identifier"""
    return "Y2025m09d28"


@pytest.fixture
def sample_build(sample_week: str) -> BuildResponse:
    """Fixture providing a single sample BuildResponse"""
    return BuildResponse(
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
    )


@pytest.fixture
def sample_builds(sample_week: str) -> List[BuildResponse]:
    """Fixture providing multiple sample BuildResponse objects"""
    return [
        BuildResponse(
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
        BuildResponse(
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
        BuildResponse(
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


@pytest.fixture
def in_memory_db():
    """Fixture providing an in-memory SQLite database connection"""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def build_repository(in_memory_db: sqlite3.Connection) -> BuildRepository:
    """Fixture providing a BuildRepository with an in-memory database"""
    repo = BuildRepository(conn=in_memory_db)

    # Create the builds table
    cursor = in_memory_db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week TEXT NOT NULL,
            pokemon TEXT,
            role TEXT,
            pkm_win_rate REAL,
            pkm_pick_rate REAL,
            move1 TEXT,
            move2 TEXT,
            moveset_win_rate REAL,
            moveset_pick_rate REAL,
            moveset_true_pick_rate REAL,
            item TEXT,
            moveset_item_win_rate REAL,
            moveset_item_pick_rate REAL,
            moveset_item_true_pick_rate REAL,
            UNIQUE(week, pokemon, move1, move2, item)
        )
        """
    )
    in_memory_db.commit()

    return repo


@pytest.fixture
def mock_build_repository(sample_builds: List[BuildResponse]) -> MagicMock:
    """Fixture providing a mocked BuildRepository"""
    mock_repo = MagicMock(spec=BuildRepository)
    mock_repo.get_all_builds.return_value = sample_builds
    mock_repo.get_available_weeks.return_value = ["Y2025m09d28"]
    mock_repo.table_name = "builds"
    return mock_repo


def create_build_response(
    id: int = 1,
    week: str = "Y2025m09d28",
    pokemon: str = "Pikachu",
    role: str = "Attacker",
    pokemon_win_rate: float = 55.0,
    pokemon_pick_rate: float = 20.0,
    move_1: str = "Thunderbolt",
    move_2: str = "Volt Tackle",
    moveset_win_rate: float = 52.0,
    moveset_pick_rate: float = 18.0,
    moveset_true_pick_rate: float = 17.0,
    item: str = "Purify",
    moveset_item_win_rate: float = 53.0,
    moveset_item_pick_rate: float = 15.0,
    moveset_item_true_pick_rate: float = 14.0,
) -> BuildResponse:
    """
    Helper function to create a BuildResponse with default values

    This is useful for tests that need to create many build instances
    with slight variations.
    """
    return BuildResponse(
        id=id,
        week=week,
        pokemon=pokemon,
        role=role,
        pokemon_win_rate=pokemon_win_rate,
        pokemon_pick_rate=pokemon_pick_rate,
        move_1=move_1,
        move_2=move_2,
        moveset_win_rate=moveset_win_rate,
        moveset_pick_rate=moveset_pick_rate,
        moveset_true_pick_rate=moveset_true_pick_rate,
        item=item,
        moveset_item_win_rate=moveset_item_win_rate,
        moveset_item_pick_rate=moveset_item_pick_rate,
        moveset_item_true_pick_rate=moveset_item_true_pick_rate,
    )
