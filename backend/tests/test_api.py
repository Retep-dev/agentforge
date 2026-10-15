from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_plan():
    response = client.post("/plan", json={"goal": "ship an evaluation suite"})
    assert response.status_code == 200
    assert len(response.json()["steps"]) == 3
