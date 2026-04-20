import os
import pytest
from dotenv import load_dotenv
from utils.api_client import APIClient

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    # This is the standard professional way: reading from environment variables
    # which are populated by the .env file or the CI/CD environment.
    return os.getenv("BASE_URL")

@pytest.fixture(scope="function")
def headers():
    token = os.getenv("API_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

@pytest.fixture(scope="function")
def api_client(base_url, headers):
    return APIClient(base_url, headers)

@pytest.fixture(scope="session", autouse=True)
def test_delete_user(base_url):
    """
    Ensures the user created during tests is deleted at the very end of the session.
    """
    yield
    user_id = os.getenv("USER_ID")
    token = os.getenv("API_TOKEN")
    
    if user_id and token:
        # We create a temporary client for the teardown to avoid scope mismatch
        client = APIClient(base_url, {"Authorization": f"Bearer {token}"})
        print(f"\n[Teardown] Deleting user: {user_id}")
        response = client.delete(f"/Account/v1/User/{user_id}")
        assert response.status_code == 204