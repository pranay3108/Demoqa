import os
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    # This is the standard professional way: reading from environment variables
    # which are populated by the .env file or the CI/CD environment.
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def headers():
    token = os.getenv("API_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }