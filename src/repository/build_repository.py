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
    Creates a new build in the database, inserting data from a BuildResponse
        object.
get_all_builds:
    Retrieves all builds from the database.

Note that the _create_table method is prefixed with an underscore, indicating
    that it is intended to be a private method, not part of the public API.
"""

import os
import sqlite3

from entity.build_model import BuildModel
from util.log import setup_custom_logger

LOG = setup_custom_logger("log_repository")


class BuildRepository:
    """
    BuildRepository class

    Args:
        table_name (str, optional): The name of the table to interact with.
            Defaults to None.
        conn (sqlite3.Connection, optional): An existing SQLite connection.
            If None, a new connection is created using the BUILDS_DB_PATH
            environment variable or defaults to 'builds.db'. Defaults to None.
    """

    def __init__(self, table_name=None, conn=None):
        LOG.info("__init__")
        LOG.debug("table_name: %s", table_name)
        LOG.debug("conn: %s", conn)

        if conn is None:
            LOG.warning("No connection provided, creating a new one")
            db_path = os.environ.get("BUILDS_DB_PATH", "builds.db")
            LOG.debug("db_path: %s", db_path)
            conn = sqlite3.connect(db_path)

        self.conn: sqlite3.Connection = conn
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.table_name: str = "builds"

    def set_table_name(self, table_name) -> None:
        """
        Set the table name

        Args:
            table_name (str): The name of the table to interact with.
        """
        LOG.info("set_table_name")
        LOG.debug("table_name: %s", table_name)

        self.table_name = table_name

    def _create_table(self) -> None:
        """
        Create the table if it does not exist
        """
        LOG.info("create_table")

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

        Returns:
            list[str]: List of table names
        """
        LOG.info("get_table_names")

        try:
            self.cursor.execute("SELECT name FROM sqlite_sequence")
        except sqlite3.OperationalError:
            LOG.error("No tables found in the database")
            return []

        LOG.info("Tables found in the database")
        table_names_query = self.cursor.fetchall()
        table_names = [table_name[0] for table_name in table_names_query]

        return table_names

    def commit(self):
        """
        Commit the changes
        """
        LOG.info("commit")

        self.conn.commit()

    def create(self, build: BuildModel, week: str, commit=True) -> bool:
        """
        Create a new build

        Args:
            build (BuildModel): The build to create
            week (str): The week identifier for the table name
            commit (bool, optional): Whether to commit the changes. Defaults to
                True.
        """
        LOG.info("create")
        LOG.debug("build: %s", build)
        LOG.debug("week: %s", week)
        LOG.debug("commit: %s", commit)

        LOG.info("Inserting build into the database")

        try:
            self.cursor.execute(
                """
                INSERT OR REPLACE INTO builds 
                (week, pokemon, role, pkm_win_rate, pkm_pick_rate, move1, move2,
                 moveset_win_rate, moveset_pick_rate, moveset_true_pick_rate,
                 item, moveset_item_win_rate, moveset_item_pick_rate,
                 moveset_item_true_pick_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    week,
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
                LOG.info("Committing changes to the database")
                self.conn.commit()

        except sqlite3.Error as error:
            LOG.error("SQLite error creating build: %s", error)
            return False

        LOG.info("BuildModel inserted successfully")

        return True

    def get_all_builds(self, week: str = None) -> list[BuildModel]:
        """
        Get all builds

        Args:
            week (str, optional): The week identifier for the builds. Defaults
                to None.

        Returns:
            list[BuildModel]: List of builds
        """
        LOG.info("get_all_builds")
        LOG.debug("week: %s", week)

        if week:
            self.cursor.execute("SELECT * FROM builds WHERE week = ?", (week,))
        else:
            self.cursor.execute("SELECT * FROM builds")

        query = self.cursor.fetchall()
        LOG.debug("query: %s", query)

        return [
            BuildModel(
                id=build[0],
                week=build[1],
                pokemon=build[2],
                role=build[3],
                pokemon_win_rate=build[4],
                pokemon_pick_rate=build[5],
                move_1=build[6],
                move_2=build[7],
                moveset_win_rate=build[8],
                moveset_pick_rate=build[9],
                moveset_true_pick_rate=build[10],
                item=build[11],
                moveset_item_win_rate=build[12],
                moveset_item_pick_rate=build[13],
                moveset_item_true_pick_rate=build[14],
            )
            for build in query
        ]

    def get_available_weeks(self) -> list[str]:
        """Get list of available weeks"""
        self.cursor.execute(
            "SELECT DISTINCT week FROM builds ORDER BY week DESC"
        )
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_pokemons_by_table(self, table_name) -> list[str]:
        """
        Get all pokemons from a table

        Args:
            table_name (str): The name of the table to interact with.

        Returns:
            list[str]: List of pokemons
        """
        LOG.info("get_all_pokemons_by_table")
        LOG.debug("table_name: %s", table_name)

        self.cursor.execute(f"SELECT pokemon FROM {table_name}")
        query = self.cursor.fetchall()

        return [pokemon[0] for pokemon in query]
