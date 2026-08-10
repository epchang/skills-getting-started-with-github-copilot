"""
Tests for GET /activities endpoint
"""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""

    def test_get_activities_returns_all_activities(self, client, fresh_activities):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 10  # 10 activities in default data

    def test_get_activities_returns_correct_activity_names(self, client, fresh_activities):
        """Test that all expected activity names are present"""
        response = client.get("/activities")
        data = response.json()
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Club",
            "Science Club",
            "Drama Club",
        ]
        for activity_name in expected_activities:
            assert activity_name in data

    def test_activity_has_correct_structure(self, client, fresh_activities):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)

    def test_participants_are_valid_emails(self, client, fresh_activities):
        """Test that all participants have valid email format"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_details in data.values():
            for email in activity_details["participants"]:
                assert "@" in email
                assert "." in email

    def test_response_content_type_is_json(self, client, fresh_activities):
        """Test that response content type is JSON"""
        response = client.get("/activities")
        assert response.headers["content-type"] == "application/json"
