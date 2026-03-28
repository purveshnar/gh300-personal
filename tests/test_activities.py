"""Test suite for Mergington High School Activities API using AAA pattern"""
import pytest


class TestGetActivities:
    """Test GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        # Arrange: client fixture is ready

        # Act: make GET request
        response = client.get("/activities")

        # Assert: verify response
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_contains_activity_details(self, client):
        # Arrange: client fixture is ready

        # Act: fetch activities
        response = client.get("/activities")
        data = response.json()

        # Assert: verify each activity has required fields
        chess_club = data["Chess Club"]
        assert chess_club["description"]
        assert chess_club["schedule"]
        assert chess_club["max_participants"] == 12
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_shows_correct_participant_count(self, client):
        # Arrange: client fixture is ready

        # Act: fetch activities
        response = client.get("/activities")
        data = response.json()

        # Assert: verify participant counts match data
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful_adds_participant(self, client, clean_activities):
        # Arrange: setup test data
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        initial_count = len(clean_activities[activity_name]["participants"])

        # Act: submit signup request
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert: verify success response and participant added
        assert response.status_code == 200
        assert email in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange: use existing participant
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act: try to sign up with existing email
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert: verify error response
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange: prepare request with invalid activity
        email = "student@mergington.edu"
        activity_name = "Nonexistent Club"

        # Act: attempt signup for non-existent activity
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            params={"email": email}
        )

        # Assert: verify not found error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Test DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful_removes_participant(self, client, clean_activities):
        # Arrange: setup with existing participant
        email = "michael@mergington.edu"
        activity_name = "Chess Club"
        initial_count = len(clean_activities[activity_name]["participants"])

        # Act: submit unregister request
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            params={"email": email}
        )

        # Assert: verify success and participant removed
        assert response.status_code == 200
        assert email not in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_non_registered_student_returns_400(self, client):
        # Arrange: use non-participant email
        email = "notregistered@mergington.edu"
        activity_name = "Chess Club"

        # Act: try to unregister someone not signed up
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            params={"email": email}
        )

        # Assert: verify error response
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        # Arrange: prepare request with invalid activity
        email = "student@mergington.edu"
        activity_name = "Nonexistent Club"

        # Act: attempt unregister from non-existent activity
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            params={"email": email}
        )

        # Assert: verify not found error
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
