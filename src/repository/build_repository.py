"""
BuildRepository class

Class Overview:

The BuildRepository class is a database abstraction layer that
manages interactions with a SQLite database containing Pokémon build data.

Class Methods:

init:
    Initializes a new BuildRepository instance, connecting to a SQLite database
        and setting the table name.
set_table_name:
    Sets the table name for the repository.
_create_table:
    Creates a new table in the database if it does not exist, with columns for
        Pokémon build data.
get_table_names:
    Retrieves a list of table names from the database.
commit:
    Commits any pending changes to the database.
create:
    Creates a new build in the database, inserting data from a Build object.
get_all_builds:
    Retrieves all builds from the database.

Note that the_create_table method is prefixed with an underscore, indicating
    that it is intended to be a private method, not part of the public API.
"""

import sqlite3

from entity.build import Build


class BuildRepository:
    """
    BuildRepository class
    """

    def __init__(self, table_name=None, conn=sqlite3.connect("builds.db")):
        self.conn: sqlite3.Connection = conn
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.table_name: str = table_name

    def set_table_name(self, table_name):
        """
        Set the table name
        """
        self.table_name = table_name

    def _create_table(self):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                moveset_item_true_pick_rate REAL
            )
            """
        )
        self.conn.commit()

    def get_table_names(self) -> list[str]:
        """
        Get the table names
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_sequence")
        except sqlite3.OperationalError:
            return []
        table_names_query = self.cursor.fetchall()
        table_names = [table_name[0] for table_name in table_names_query]
        return table_names

    def commit(self):
        """
        Commit the changes
        """
        self.conn.commit()

    def create(self, build: Build, commit=True):
        """
        Create a new build
        """
        if not self.table_name:
            print("Table name not set")
            return False
        try:
            self._create_table()
            self.cursor.execute(
                f"""
                INSERT INTO {self.table_name} (pokemon, role, pkm_win_rate, pkm_pick_rate, move1, move2, moveset_win_rate, moveset_pick_rate, moveset_true_pick_rate, item, moveset_item_win_rate, moveset_item_pick_rate, moveset_item_true_pick_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    build.pokemon,
                    build.role,
                    build.pokemon_win_rate,
                    build.pokemon_pick_rate,
                    build.move_1,
                    build.move_2,
                    build.moveset_win_rate,
                    build.moveset_pick_rate,
                    build.moveset_true_pick_rate,
                    build.item,
                    build.moveset_item_win_rate,
                    build.moveset_item_pick_rate,
                    build.moveset_item_true_pick_rate,
                ),
            )

            if commit:
                self.conn.commit()

        except sqlite3.OperationalError:
            print("Table name not set")
            return False

        return True

    def get_all_builds_by_table(self, table_name) -> list[Build]:
        """
        Get all builds
        """
        self.cursor.execute(f"SELECT * FROM {table_name}")
        query = self.cursor.fetchall()

        return [
            Build(
                pokemon=build[1],
                role=build[2],
                pokemon_win_rate=build[3],
                pokemon_pick_rate=build[4],
                move_1=build[5],
                move_2=build[6],
                moveset_win_rate=build[7],
                moveset_pick_rate=build[8],
                moveset_true_pick_rate=build[9],
                item=build[10],
                moveset_item_win_rate=build[11],
                moveset_item_pick_rate=build[12],
                moveset_item_true_pick_rate=build[13],
            )
            for build in query
        ]

    def get_all_pokemons_by_table(self, table_name) -> list[str]:
        """
        Get all pokemons from a table
        """
        self.cursor.execute(f"SELECT pokemon FROM {table_name}")
        query = self.cursor.fetchall()

        return [pokemon[0] for pokemon in query]
