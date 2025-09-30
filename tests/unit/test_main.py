from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app
from entity.build_response import BuildResponse
from src.api.builds_query_params import BuildsQueryParams

client = TestClient(app)


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


# /builds endpoint tests
# These tests assume BuildRepository and strategies are working and database is populated.
# For real unit tests, mocking BuildRepository is recommended.


class DummyBuild:
    def __init__(self):
        self.pokemon = "Pikachu"
        self.role = "Attacker"
        self.pokemon_win_rate = 55.0
        self.pokemon_pick_rate = 20.0
        self.move_1 = "Thunderbolt"
        self.move_2 = "Volt Tackle"
        self.moveset_win_rate = 52.0
        self.moveset_pick_rate = 18.0
        self.moveset_true_pick_rate = 17.0
        self.item = "Wise Glasses"
        self.moveset_item_win_rate = 53.0
        self.moveset_item_pick_rate = 15.0
        self.moveset_item_true_pick_rate = 14.0


@patch("src.api.main.BuildRepository")
def test_top_n_limit(mock_repo):
    # Prepare 5 dummy builds
    dummy_builds = [DummyBuild() for _ in range(5)]
    instance = mock_repo.return_value
    instance.get_all_builds_by_table.return_value = dummy_builds
    instance.table_name = "dummy"

    params = BuildsQueryParams(top_n=2)
    from src.api.main import get_builds

    result = get_builds(params)
    assert isinstance(result, list)
    assert len(result) == 2
    for build in result:
        assert isinstance(build, BuildResponse)


def test_get_builds_default(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Pikachu"
            self.role = "Attacker"
            self.pokemon_win_rate = 55.0
            self.pokemon_pick_rate = 20.0
            self.move_1 = "Thunderbolt"
            self.move_2 = "Volt Tackle"
            self.moveset_win_rate = 52.0
            self.moveset_pick_rate = 18.0
            self.moveset_true_pick_rate = 17.0
            self.item = "Wise Glasses"
            self.moveset_item_win_rate = 53.0
            self.moveset_item_pick_rate = 15.0
            self.moveset_item_true_pick_rate = 14.0

    dummy_builds = [DummyBuild(0), DummyBuild(1)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["pokemon"] == "Pikachu"
    assert data[0]["role"] == "Attacker"


def test_get_builds_by_id(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Snorlax"
            self.role = "Defender"
            self.pokemon_win_rate = 50.0
            self.pokemon_pick_rate = 15.0
            self.move_1 = "Tackle"
            self.move_2 = "Block"
            self.moveset_win_rate = 48.0
            self.moveset_pick_rate = 13.0
            self.moveset_true_pick_rate = 12.0
            self.item = "Leftovers"
            self.moveset_item_win_rate = 49.0
            self.moveset_item_pick_rate = 10.0
            self.moveset_item_true_pick_rate = 9.0

    dummy_builds = [DummyBuild(0), DummyBuild(1)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?id=1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["pokemon"] == "Snorlax"
    assert data[0]["role"] == "Defender"


def test_get_builds_invalid_strategy(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Lucario"
            self.role = "All-Rounder"
            self.pokemon_win_rate = 60.0
            self.pokemon_pick_rate = 25.0
            self.move_1 = "Power-Up Punch"
            self.move_2 = "Bone Rush"
            self.moveset_win_rate = 58.0
            self.moveset_pick_rate = 22.0
            self.moveset_true_pick_rate = 21.0
            self.item = "Muscle Band"
            self.moveset_item_win_rate = 59.0
            self.moveset_item_pick_rate = 20.0
            self.moveset_item_true_pick_rate = 19.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?sort_by=not_a_strategy")

    # Assert
    assert response.status_code == 400


def test_get_builds_invalid_relevance(monkeypatch, caplog):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Pikachu"
            self.role = "Attacker"
            self.pokemon_win_rate = 55.0
            self.pokemon_pick_rate = 20.0
            self.move_1 = "Thunderbolt"
            self.move_2 = "Volt Tackle"
            self.moveset_win_rate = 52.0
            self.moveset_pick_rate = 18.0
            self.moveset_true_pick_rate = 17.0
            self.item = "Wise Glasses"
            self.moveset_item_win_rate = 53.0
            self.moveset_item_pick_rate = 15.0
            self.moveset_item_true_pick_rate = 14.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )
    # Act
    response = client.get("/builds?relevance=not_a_strategy")

    # Assert
    assert response.status_code == 400


def test_get_builds_filter_pokemon(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Pikachu"
            self.role = "Attacker"
            self.pokemon_win_rate = 55.0
            self.pokemon_pick_rate = 20.0
            self.move_1 = "Thunderbolt"
            self.move_2 = "Volt Tackle"
            self.moveset_win_rate = 52.0
            self.moveset_pick_rate = 18.0
            self.moveset_true_pick_rate = 17.0
            self.item = "Wise Glasses"
            self.moveset_item_win_rate = 53.0
            self.moveset_item_pick_rate = 15.0
            self.moveset_item_true_pick_rate = 14.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?pokemon=Pikachu")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["pokemon"] == "Pikachu"


def test_get_builds_filter_ignore_pokemon(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Snorlax"
            self.role = "Defender"
            self.pokemon_win_rate = 50.0
            self.pokemon_pick_rate = 15.0
            self.move_1 = "Tackle"
            self.move_2 = "Block"
            self.moveset_win_rate = 48.0
            self.moveset_pick_rate = 13.0
            self.moveset_true_pick_rate = 12.0
            self.item = "Leftovers"
            self.moveset_item_win_rate = 49.0
            self.moveset_item_pick_rate = 10.0
            self.moveset_item_true_pick_rate = 9.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?ignore_pokemon=Snorlax")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_builds_filter_role(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Lucario"
            self.role = "All-Rounder"
            self.pokemon_win_rate = 60.0
            self.pokemon_pick_rate = 25.0
            self.move_1 = "Power-Up Punch"
            self.move_2 = "Bone Rush"
            self.moveset_win_rate = 58.0
            self.moveset_pick_rate = 22.0
            self.moveset_true_pick_rate = 21.0
            self.item = "Muscle Band"
            self.moveset_item_win_rate = 59.0
            self.moveset_item_pick_rate = 20.0
            self.moveset_item_true_pick_rate = 19.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?role=All-Rounder")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["role"] == "All-Rounder"


def test_get_builds_filter_ignore_role(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Lucario"
            self.role = "All-Rounder"
            self.pokemon_win_rate = 60.0
            self.pokemon_pick_rate = 25.0
            self.move_1 = "Power-Up Punch"
            self.move_2 = "Bone Rush"
            self.moveset_win_rate = 58.0
            self.moveset_pick_rate = 22.0
            self.moveset_true_pick_rate = 21.0
            self.item = "Muscle Band"
            self.moveset_item_win_rate = 59.0
            self.moveset_item_pick_rate = 20.0
            self.moveset_item_true_pick_rate = 19.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?ignore_role=All-Rounder")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_builds_filter_item(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Lucario"
            self.role = "All-Rounder"
            self.pokemon_win_rate = 60.0
            self.pokemon_pick_rate = 25.0
            self.move_1 = "Power-Up Punch"
            self.move_2 = "Bone Rush"
            self.moveset_win_rate = 58.0
            self.moveset_pick_rate = 22.0
            self.moveset_true_pick_rate = 21.0
            self.item = "Muscle Band"
            self.moveset_item_win_rate = 59.0
            self.moveset_item_pick_rate = 20.0
            self.moveset_item_true_pick_rate = 19.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?item=Muscle Band")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["item"] == "Muscle Band"


def test_get_builds_filter_ignore_item(monkeypatch):
    # Arrange
    class DummyBuild:
        def __init__(self, id):
            self.id = id
            self.pokemon = "Lucario"
            self.role = "All-Rounder"
            self.pokemon_win_rate = 60.0
            self.pokemon_pick_rate = 25.0
            self.move_1 = "Power-Up Punch"
            self.move_2 = "Bone Rush"
            self.moveset_win_rate = 58.0
            self.moveset_pick_rate = 22.0
            self.moveset_true_pick_rate = 21.0
            self.item = "Muscle Band"
            self.moveset_item_win_rate = 59.0
            self.moveset_item_pick_rate = 20.0
            self.moveset_item_true_pick_rate = 19.0

    dummy_builds = [DummyBuild(0)]
    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.get_all_builds_by_table",
        lambda self, table: dummy_builds,
    )

    def build_repo_init(self):
        self.table_name = "dummy_table"
        self.conn = None
        self.cursor = None

    monkeypatch.setattr(
        "repository.build_repository.BuildRepository.__init__", build_repo_init
    )

    # Act
    response = client.get("/builds?ignore_item=Muscle Band")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
