import os
import logging
from utils.helper import update_env_variable

logger = logging.getLogger(__name__)
username='BookAPIUSERS1'
password='Password@123'

def test_post_user(api_client):
    user_response = api_client.post("/Account/v1/User", json={
        "userName": username,
        "password": password
    })
    logger.info(user_response.json())
    assert user_response.status_code == 201
    assert user_response.json().get("username") == username
    user_id = user_response.json().get("userID")
    logger.info(f"User ID: {user_id}")
    assert user_id is not None

    # ✅ Write userId to .env
    update_env_variable("USER_ID", user_id)



def test_post_generate_token(api_client):
    token_response = api_client.post("/Account/v1/GenerateToken", json={
        "userName": username,
        "password": password
    })
    assert token_response.status_code == 200
    assert token_response.json().get("status") == "Success" 
    token = token_response.json().get("token")
    assert token is not None

    # ✅ Write token to .env
    update_env_variable("API_TOKEN", token)


def test_post_authorized(api_client):
    user_auth_response = api_client.post("/Account/v1/Authorized", json={
        "userName": username,
        "password": password
    })
    assert user_auth_response.status_code == 200
    assert user_auth_response.json() == True

    

def test_get_user(api_client):
    user_id = os.getenv("USER_ID")
    user_response = api_client.get(f"/Account/v1/User/{user_id}")
    assert user_response.status_code == 200
    assert user_response.json().get("username") == username
