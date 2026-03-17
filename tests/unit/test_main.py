from unittest.mock import MagicMock, patch

from conftest import create_build_response
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def _create_mock_repository():
    """Helper to create a mock repository with context manager support"""
    mock = MagicMock()
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def test_read_root():
    # Arrange & Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "debug" in data
    assert "host" in data
    assert "port" in data
    assert data["message"].endswith("is running.")


def test_health_check():
    # Arrange & Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_weeks():
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [
            "Y2025m09d28",
            "Y2025m10d05",
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/weeks")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "Y2025m09d28" in data
        assert "Y2025m10d05" in data


def test_get_builds_default(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week, pokemon="Pikachu"),
            create_build_response(id=2, week=sample_week, pokemon="Snorlax"),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["pokemon"] == "Pikachu"
        assert data[1]["pokemon"] == "Snorlax"


def test_get_builds_by_id(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week, pokemon="Pikachu"),
            create_build_response(id=2, week=sample_week, pokemon="Snorlax"),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?id=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["pokemon"] == "Snorlax"


def test_get_builds_by_week(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [
            sample_week,
            "Y2025m10d05",
        ]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week, pokemon="Pikachu"),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get(f"/builds?week={sample_week}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["week"] == sample_week


def test_get_builds_invalid_week(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?week=Y2099m01d01")

        # Assert
        assert response.status_code == 400
        assert "Invalid week" in response.json()["detail"]


def test_get_builds_invalid_strategy(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?sort_by=not_a_strategy")

        # Assert
        assert response.status_code == 400


def test_get_builds_invalid_relevance(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?relevance=not_a_strategy")

        # Assert
        assert response.status_code == 400


def test_get_builds_filter_pokemon(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week, pokemon="Pikachu"),
            create_build_response(id=2, week=sample_week, pokemon="Snorlax"),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?pokemon=Pikachu")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["pokemon"] == "Pikachu"


def test_get_builds_filter_ignore_pokemon(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=1, week=sample_week, pokemon="Pikachu"),
            create_build_response(id=2, week=sample_week, pokemon="Snorlax"),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?ignore_pokemon=Snorlax")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["pokemon"] == "Pikachu"


def test_get_builds_filter_role(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(
                id=1, week=sample_week, pokemon="Pikachu", role="Attacker"
            ),
            create_build_response(
                id=2, week=sample_week, pokemon="Snorlax", role="Defender"
            ),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?role=Defender")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["role"] == "Defender"


def test_get_builds_filter_ignore_role(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(
                id=1, week=sample_week, pokemon="Pikachu", role="Attacker"
            ),
            create_build_response(
                id=2, week=sample_week, pokemon="Snorlax", role="Defender"
            ),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?ignore_role=Attacker")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["role"] == "Defender"


def test_get_builds_filter_item(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(
                id=1, week=sample_week, pokemon="Pikachu", item="Purify"
            ),
            create_build_response(
                id=2, week=sample_week, pokemon="Snorlax", item="ShedinjaDoll"
            ),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?item=Purify")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["item"] == "Purify"


def test_get_builds_filter_ignore_item(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(
                id=1, week=sample_week, pokemon="Pikachu", item="Purify"
            ),
            create_build_response(
                id=2, week=sample_week, pokemon="Snorlax", item="ShedinjaDoll"
            ),
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?ignore_item=ShedinjaDoll")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["item"] == "Purify"


def test_get_builds_top_n(sample_week):
    # Arrange
    with patch("api.main.BuildRepository") as mock_repo_class:
        mock_repo = _create_mock_repository()
        mock_repo.get_available_weeks.return_value = [sample_week]
        mock_repo.get_all_builds.return_value = [
            create_build_response(id=i, week=sample_week, pokemon=f"Pokemon{i}")
            for i in range(10)
        ]
        mock_repo_class.return_value = mock_repo

        # Act
        response = client.get("/builds?top_n=3")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
