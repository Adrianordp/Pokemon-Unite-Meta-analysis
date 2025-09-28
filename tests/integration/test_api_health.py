from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_server_startup():
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
