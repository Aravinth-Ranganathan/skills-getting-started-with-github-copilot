from fastapi.testclient import TestClient

from src.app import app


def test_unregister_participant_removes_participant_from_activity():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess%20Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "Unregistered michael@mergington.edu" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
