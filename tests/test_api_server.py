from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_address_found():
    response = client.get("/api/v1/address/1000001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["prefecture"] == "東京都"
    assert data[0]["city"] == "千代田区"


def test_address_with_hyphen():
    response = client.get("/api/v1/address/100-0001")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["prefecture"] == "東京都"


def test_address_not_found():
    response = client.get("/api/v1/address/0000000")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
