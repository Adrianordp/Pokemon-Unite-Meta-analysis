"""Unit tests for CLI client."""

from unittest.mock import MagicMock, patch

import pytest  # noqa: E402

# Import the main module directly, not via __init__
from cli.main import (  # noqa: E402
    colorize_role,
    get_builds,
    get_health,
    main,
)


@pytest.fixture
def mock_httpx_get():
    """Mock httpx.get for testing."""
    with patch("cli.main.httpx.get") as mock_get:
        yield mock_get


class TestGetHealth:
    """Tests for get_health function."""

    def test_get_health_success(self, mock_httpx_get, capsys):
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "ok"}
        mock_httpx_get.return_value = mock_response

        get_health()

        out = capsys.readouterr().out
        assert "API Health" in out
        assert "ok" in out
        mock_httpx_get.assert_called_once()

    def test_get_health_failure(self, mock_httpx_get):
        """Test health check failure."""
        mock_httpx_get.side_effect = Exception("Connection failed")

        with pytest.raises(SystemExit) as exc_info:
            get_health()

        assert exc_info.value.code == 1

    def test_get_health_http_error(self, mock_httpx_get):
        """Test health check with HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_httpx_get.return_value = mock_response

        with pytest.raises(SystemExit) as exc_info:
            get_health()

        assert exc_info.value.code == 1


class TestColorizeRole:
    """Tests for colorize_role function."""

    def test_colorize_role_attacker(self):
        """Test colorizing Attacker role."""
        text = "Venusaur Attacker"
        colored = colorize_role(text)
        assert "\033[38;5;1m" in colored  # Red for Attacker
        assert "\033[0m" in colored  # Reset code

    def test_colorize_role_support(self):
        """Test colorizing Support role."""
        text = "Clefable Support"
        colored = colorize_role(text)
        assert "\033[38;5;214m" in colored  # Orange for Support

    def test_colorize_role_defender(self):
        """Test colorizing Defender role."""
        text = "Blastoise Defender"
        colored = colorize_role(text)
        assert "\033[1;38;5;2m" in colored  # Green for Defender

    def test_colorize_role_speedster(self):
        """Test colorizing Speedster role."""
        text = "Zoroark Speedster"
        colored = colorize_role(text)
        assert "\033[38;5;4m" in colored  # Blue for Speedster

    def test_colorize_role_all_rounder(self):
        """Test colorizing All-Rounder role."""
        text = "Lucario All-Rounder"
        colored = colorize_role(text)
        assert "\033[38;5;93m" in colored  # Purple for All-Rounder

    def test_colorize_role_multiple_roles(self):
        """Test colorizing text with multiple roles."""
        text = "Venusaur Attacker\nClefable Support\nBlastoise Defender\nZoroark Speedster\nLucario All-Rounder"
        colored = colorize_role(text)
        assert "\033[38;5;1m" in colored  # Attacker
        assert "\033[38;5;214m" in colored  # Support
        assert "\033[1;38;5;2m" in colored  # Defender
        assert "\033[38;5;4m" in colored  # Speedster
        assert "\033[38;5;93m" in colored  # All-Rounder

    def test_colorize_role_case_insensitive(self):
        """Test that colorization is case-insensitive."""
        text_lower = "venusaur attacker"
        text_upper = "VENUSAUR ATTACKER"
        colored_lower = colorize_role(text_lower)
        colored_upper = colorize_role(text_upper)
        assert "\033[38;5;1m" in colored_lower
        assert "\033[38;5;1m" in colored_upper


class TestGetBuilds:
    """Tests for get_builds function."""

    def test_get_builds_success(self, mock_httpx_get, capsys):
        """Test successful builds retrieval."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Venusaur",
                "role": "Attacker",
                "moveset_item_win_rate": 52.77,
                "week": "Y2025m10d05",
            },
            {
                "id": 2,
                "pokemon": "Clefable",
                "role": "Support",
                "moveset_item_win_rate": 51.85,
                "week": "Y2025m10d05",
            },
        ]
        mock_httpx_get.return_value = mock_response

        get_builds(params={"week": "Y2025m10d05"})

        out = capsys.readouterr().out
        assert "Venusaur" in out
        assert "Clefable" in out
        assert "Attacker" in out
        assert "Support" in out
        mock_httpx_get.assert_called_once()

    def test_get_builds_with_include_columns(self, mock_httpx_get, capsys):
        """Test builds retrieval with column inclusion."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Venusaur",
                "role": "Attacker",
                "moveset_item_win_rate": 52.77,
                "week": "Y2025m10d05",
            }
        ]
        mock_httpx_get.return_value = mock_response

        get_builds(
            params=None,
            include=["pokemon", "role", "moveset_item_win_rate"],
            exclude=None,
        )

        out = capsys.readouterr().out
        assert "Pokemon" in out  # Renamed column
        assert "Venusaur" in out
        assert "Attacker" in out
        # ID and Week should not be in output since not included
        assert "ID" not in out or "Week" not in out

    def test_get_builds_with_exclude_columns(self, mock_httpx_get, capsys):
        """Test builds retrieval with column exclusion."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Venusaur",
                "role": "Attacker",
                "moveset_item_win_rate": 52.77,
                "week": "Y2025m10d05",
            }
        ]
        mock_httpx_get.return_value = mock_response

        get_builds(params=None, include=None, exclude=["id", "week"])

        out = capsys.readouterr().out
        assert "Venusaur" in out
        assert "Attacker" in out
        # Excluded columns should not appear
        assert out.count("ID") == 0 or "ID" not in out.split("\n")[0]

    def test_get_builds_no_builds(self, mock_httpx_get, capsys):
        """Test builds retrieval when no builds are found."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = []
        mock_httpx_get.return_value = mock_response

        get_builds(params=None)

        out = capsys.readouterr().out
        assert "No builds found." in out

    def test_get_builds_failure(self, mock_httpx_get):
        """Test builds retrieval failure."""
        mock_httpx_get.side_effect = Exception("Connection failed")

        with pytest.raises(SystemExit) as exc_info:
            get_builds(params=None)

        assert exc_info.value.code == 1

    def test_get_builds_http_error(self, mock_httpx_get):
        """Test builds retrieval with HTTP error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception(
            "500 Server Error"
        )
        mock_httpx_get.return_value = mock_response

        with pytest.raises(SystemExit) as exc_info:
            get_builds(params=None)

        assert exc_info.value.code == 1

    def test_get_builds_with_params(self, mock_httpx_get, capsys):
        """Test builds retrieval with query parameters."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Pikachu",
                "role": "Attacker",
                "moveset_item_win_rate": 53.5,
                "week": "Y2025m10d05",
            }
        ]
        mock_httpx_get.return_value = mock_response

        params = {
            "pokemon": "Pikachu",
            "week": "Y2025m10d05",
            "relevance": "top_n",
            "relevance_threshold": 10,
            "sort_by": "moveset_item_win_rate",
        }
        get_builds(params=params)

        out = capsys.readouterr().out
        assert "Pikachu" in out
        mock_httpx_get.assert_called_once_with(
            "http://localhost:8000/builds", params=params
        )


class TestMain:
    """Tests for main function."""

    def test_main_health_command(self, mock_httpx_get, capsys):
        """Test main with health command."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "ok"}
        mock_httpx_get.return_value = mock_response

        with patch("sys.argv", ["cli", "health"]):
            main()

        out = capsys.readouterr().out
        assert "API Health" in out
        assert "ok" in out

    def test_main_get_builds_command(self, mock_httpx_get, capsys):
        """Test main with get-builds command."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Venusaur",
                "role": "Attacker",
                "moveset_item_win_rate": 52.77,
                "week": "Y2025m10d05",
            }
        ]
        mock_httpx_get.return_value = mock_response

        with patch("sys.argv", ["cli", "get-builds", "--week", "Y2025m10d05"]):
            main()

        out = capsys.readouterr().out
        assert "Venusaur" in out

    def test_main_get_builds_with_filters(self, mock_httpx_get, capsys):
        """Test main with get-builds command and filters."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Clefable",
                "role": "Support",
                "moveset_item_win_rate": 51.85,
                "week": "Y2025m10d05",
            }
        ]
        mock_httpx_get.return_value = mock_response

        with patch(
            "sys.argv",
            [
                "cli",
                "get-builds",
                "--role",
                "Support",
                "--week",
                "Y2025m10d05",
                "--relevance",
                "top_n",
                "--relevance-threshold",
                "10",
                "--sort-by",
                "moveset_item_win_rate",
            ],
        ):
            main()

        out = capsys.readouterr().out
        assert "Clefable" in out
        assert "Support" in out

    def test_main_get_builds_with_column_selection(
        self, mock_httpx_get, capsys
    ):
        """Test main with get-builds command and column selection."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "pokemon": "Venusaur",
                "role": "Attacker",
                "moveset_item_win_rate": 52.77,
                "week": "Y2025m10d05",
            }
        ]
        mock_httpx_get.return_value = mock_response

        with patch(
            "sys.argv",
            [
                "cli",
                "get-builds",
                "--include",
                "pokemon",
                "role",
                "moveset_item_win_rate",
            ],
        ):
            main()

        out = capsys.readouterr().out
        assert "Pokemon" in out
        assert "Venusaur" in out

    def test_main_invalid_command(self):
        """Test main with invalid command."""
        with patch("sys.argv", ["cli"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            # argparse exits with code 2 for invalid arguments
            assert exc_info.value.code == 2

    def test_main_help(self):
        """Test main with --help flag."""
        with patch("sys.argv", ["cli", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            # argparse exits with code 0 for help
            assert exc_info.value.code == 0

    def test_main_get_builds_help(self):
        """Test main with get-builds --help."""
        with patch("sys.argv", ["cli", "get-builds", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
