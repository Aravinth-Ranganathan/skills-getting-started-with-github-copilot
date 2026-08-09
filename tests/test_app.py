import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_state))


def test_get_activities_returns_activity_catalog():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"]


def test_signup_for_activity_adds_participant():
    # Arrange
    client = TestClient(app_module.app)
    email = "teststudent@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_error():
    # Arrange
    client = TestClient(app_module.app)
    email = "dupe@mergington.edu"

    # Act
    client.post(f"/activities/Chess Club/signup?email={email}")
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_participant_removes_participant_from_activity():
    # Arrange
    client = TestClient(app_module.app)
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
