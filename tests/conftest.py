"""
Shared fixtures and configuration for API tests
"""
import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the initial state of activities at module load time
_INITIAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the API"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Reset activities to a clean state before each test for test isolation"""
    # Clear and reset to initial state before test
    activities.clear()
    activities.update(deepcopy(_INITIAL_ACTIVITIES))
    yield activities
    # Cleanup: restore initial state after test
    activities.clear()
    activities.update(deepcopy(_INITIAL_ACTIVITIES))


@pytest.fixture
def sample_activity_name():
    """Provide a valid activity name for testing"""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Provide a sample email for testing"""
    return "test_student@mergington.edu"
