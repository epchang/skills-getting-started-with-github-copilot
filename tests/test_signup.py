"""
Tests for POST /activities/{activity_name}/signup endpoint
"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up for an activity"""

    def test_signup_new_participant_succeeds(self, client, fresh_activities, sample_activity_name, sample_email):
        """Test successful signup for a new participant"""
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert sample_activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, fresh_activities, sample_activity_name, sample_email):
        """Test that signup actually adds the participant to the activity"""
        # Sign up the participant
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Verify participant was added
        response = client.get("/activities")
        activities = response.json()
        assert sample_email in activities[sample_activity_name]["participants"]

    def test_signup_increases_participant_count(self, client, fresh_activities, sample_activity_name, sample_email):
        """Test that signup increases the participant count"""
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()[sample_activity_name]["participants"])
        
        # Sign up new participant
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        
        # Verify count increased
        response = client.get("/activities")
        new_count = len(response.json()[sample_activity_name]["participants"])
        assert new_count == initial_count + 1

    def test_signup_duplicate_participant_returns_400(self, client, fresh_activities, sample_activity_name):
        """Test that signing up twice with same email returns 400"""
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": existing_email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client, fresh_activities, sample_email):
        """Test that signing up for non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_signup_with_special_characters_in_email(self, client, fresh_activities, sample_activity_name):
        """Test signup with email containing special characters"""
        special_email = "test+special@mergington.edu"
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": special_email}
        )
        assert response.status_code == 200
        
        # Verify it was added
        response = client.get("/activities")
        activities = response.json()
        assert special_email in activities[sample_activity_name]["participants"]

    def test_signup_response_message_format(self, client, fresh_activities, sample_activity_name, sample_email):
        """Test that success response message has correct format"""
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        data = response.json()
        assert "Signed up" in data["message"]
        assert sample_email in data["message"]
        assert "for" in data["message"]
        assert sample_activity_name in data["message"]

    def test_signup_multiple_participants_same_activity(self, client, fresh_activities, sample_activity_name):
        """Test that multiple different participants can sign up for same activity"""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email2}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both were added
        response = client.get("/activities")
        activities = response.json()
        assert email1 in activities[sample_activity_name]["participants"]
        assert email2 in activities[sample_activity_name]["participants"]
