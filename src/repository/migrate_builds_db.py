"""
Migrate builds database from multiple tables to single table with week column
"""

import os
import sqlite3

from util.log import setup_custom_logger

LOG = setup_custom_logger("log_migration")


def migrate_to_single_table():
    """Migrate from per-week tables to single table with week column"""
    db_path = os.environ.get("BUILDS_DB_PATH", "builds.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create new builds table
    cursor.execute("""
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
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_builds_week ON builds(week)")

    # Get all weekly tables
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Y%'"
    )
    tables = cursor.fetchall()

    # Migrate data from each table
    for (table_name,) in tables:
        LOG.info(f"Migrating table: {table_name}")

        cursor.execute(f"""
            INSERT OR IGNORE INTO builds 
            (week, pokemon, role, pkm_win_rate, pkm_pick_rate, move1, move2, 
             moveset_win_rate, moveset_pick_rate, moveset_true_pick_rate, 
             item, moveset_item_win_rate, moveset_item_pick_rate, 
             moveset_item_true_pick_rate)
            SELECT 
                '{table_name}' as week,
                pokemon, role, pkm_win_rate, pkm_pick_rate, move1, move2,
                moveset_win_rate, moveset_pick_rate, moveset_true_pick_rate,
                item, moveset_item_win_rate, moveset_item_pick_rate,
                moveset_item_true_pick_rate
            FROM {table_name}
        """)

        count = cursor.rowcount
        LOG.info(f"Migrated {count} rows from {table_name}")

    conn.commit()

    # Optional: Drop old tables after verification
    # for (table_name,) in tables:
    #     cursor.execute(f"DROP TABLE {table_name}")

    conn.close()
    LOG.info("Migration complete")


if __name__ == "__main__":
    migrate_to_single_table()
