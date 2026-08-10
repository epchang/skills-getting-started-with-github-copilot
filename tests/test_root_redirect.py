"""
Tests for GET / redirect endpoint
"""
import pytest


class TestRootRedirect:
    """Test suite for root path redirect"""

    def test_root_path_redirects_to_static_index(self, client, fresh_activities):
        """Test that GET / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        # FastAPI redirects with 307 Temporary Redirect
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]

    def test_root_path_final_redirect_follows_to_static(self, client, fresh_activities):
        """Test that following redirect reaches static index"""
        response = client.get("/", follow_redirects=True)
        # When following redirects, we should get a response (though it may be from the static mount)
        # The TestClient will follow the redirect
        assert response.status_code in [200, 304]  # 200 OK or 304 Not Modified

    def test_root_redirect_has_location_header(self, client, fresh_activities):
        """Test that redirect response includes Location header"""
        response = client.get("/", follow_redirects=False)
        assert "location" in response.headers
        assert response.headers["location"].endswith("/static/index.html")

    def test_root_path_is_not_found_in_main_app(self, client, fresh_activities):
        """Test that root path without redirect would not be a normal route"""
        # This test verifies that root must redirect (not return 404)
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
