import os
import random
from dotenv import dotenv_values, set_key
from pathlib import Path

ENV_FILE_PATH = Path(".env")  # adjust path if needed


def update_env_variable(key: str, value: str):
    """
    Update or add a variable in the .env file
    """
    if not ENV_FILE_PATH.exists():
        ENV_FILE_PATH.touch()

    set_key(dotenv_path=ENV_FILE_PATH, key_to_set=key, value_to_set=value)
    os.environ[key] = value

