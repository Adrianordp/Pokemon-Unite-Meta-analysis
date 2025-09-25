import subprocess
import sys
import os
import tempfile
import shutil
import pytest

# Integration test for CLI workflow: end-to-end data retrieval

def test_cli_print_sorted_data(monkeypatch):
    """
    Runs the CLI entrypoint and checks that output contains expected columns.
    Uses a temporary copy of the database to avoid modifying real data.
    """
    # Path to CLI entrypoint
    cli_path = os.path.join(os.path.dirname(__file__), '../../src/pokemon_unite_meta_analysis/__main__.py')
    cli_path = os.path.abspath(cli_path)
    db_path = os.path.join(os.path.dirname(__file__), '../../builds.db')
    db_path = os.path.abspath(db_path)

    # Use a temp dir for DB to avoid side effects
    with tempfile.TemporaryDirectory() as tmpdir:
        test_db = os.path.join(tmpdir, 'builds.db')
        shutil.copy(db_path, test_db)
        monkeypatch.setenv('BUILDS_DB_PATH', test_db)

        # Run the CLI as a subprocess
        result = subprocess.run(
            [sys.executable, cli_path],
            capture_output=True,
            text=True,
            env=os.environ,
            timeout=20
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        # Check for expected output columns
        assert "Pokemon" in result.stdout
        assert "Role" in result.stdout
        assert "M&I_WR" in result.stdout
        assert "M&I_@PR" in result.stdout
