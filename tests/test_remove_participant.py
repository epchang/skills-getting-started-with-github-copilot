"""
Tests for DELETE /activities/{activity_name}/participant endpoint
"""
import pytest


class TestRemoveParticipant:
    """Test suite for removing a participant from an activity"""

    def test_remove_existing_participant_succeeds(self, client, fresh_activities, sample_activity_name):
        """Test successful removal of an existing participant"""
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": existing_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert existing_email in data["message"]

    def test_remove_participant_removes_from_activity(self, client, fresh_activities, sample_activity_name):
        """Test that remove actually removes the participant"""
        existing_email = "michael@mergington.edu"
        
        # Remove the participant
        client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": existing_email}
        )
        
        # Verify participant was removed
        response = client.get("/activities")
        activities = response.json()
        assert existing_email not in activities[sample_activity_name]["participants"]

    def test_remove_decreases_participant_count(self, client, fresh_activities, sample_activity_name):
        """Test that remove decreases the participant count"""
        existing_email = "michael@mergington.edu"
        
        # Get initial count
        response = client.get("/activities")
        initial_count = len(response.json()[sample_activity_name]["participants"])
        
        # Remove participant
        client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": existing_email}
        )
        
        # Verify count decreased
        response = client.get("/activities")
        new_count = len(response.json()[sample_activity_name]["participants"])
        assert new_count == initial_count - 1

    def test_remove_nonexistent_participant_returns_400(self, client, fresh_activities, sample_activity_name):
        """Test that removing non-existent participant returns 400"""
        nonexistent_email = "nothere@mergington.edu"
        
        response = client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": nonexistent_email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_returns_404(self, client, fresh_activities, sample_email):
        """Test that removing from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent Activity/participant",
            params={"email": sample_email}
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_remove_response_message_format(self, client, fresh_activities, sample_activity_name):
        """Test that success response message has correct format"""
        existing_email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": existing_email}
        )
        data = response.json()
        assert "Removed" in data["message"]
        assert existing_email in data["message"]
        assert "from" in data["message"]
        assert sample_activity_name in data["message"]

    def test_remove_multiple_participants_sequentially(self, client, fresh_activities):
        """Test removing multiple participants from same activity"""
        activity = "Music Band"  # Has lucas and sophia
        email1 = "lucas@mergington.edu"
        email2 = "sophia@mergington.edu"
        
        # Remove first participant
        response1 = client.delete(
            f"/activities/{activity}/participant",
            params={"email": email1}
        )
        assert response1.status_code == 200
        
        # Remove second participant
        response2 = client.delete(
            f"/activities/{activity}/participant",
            params={"email": email2}
        )
        assert response2.status_code == 200
        
        # Verify both were removed
        response = client.get("/activities")
        activities = response.json()
        assert email1 not in activities[activity]["participants"]
        assert email2 not in activities[activity]["participants"]

    def test_remove_cannot_remove_same_participant_twice(self, client, fresh_activities, sample_activity_name):
        """Test that removing same participant twice fails on second attempt"""
        existing_email = "michael@mergington.edu"
        
        # First removal succeeds
        response1 = client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": existing_email}
        )
        assert response1.status_code == 200
        
        # Second removal fails
        response2 = client.delete(
            f"/activities/{sample_activity_name}/participant",
            params={"email": existing_email}
        )
        assert response2.status_code == 400
