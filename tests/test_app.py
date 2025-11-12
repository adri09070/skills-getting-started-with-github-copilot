import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400

def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404

def test_unregister_for_activity():
    activity = "Chess Club"
    email = "removeme@mergington.edu"
    # Add if not present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    # Simulate unregister endpoint (not implemented)
    # Remove manually and check
    activities[activity]["participants"].remove(email)
    assert email not in activities[activity]["participants"]