"""Ger apy_id for get weather for city."""
from pathlib import Path
import os
from dotenv import load_dotenv


def get_apy_id():
    """Get apy_id from '.flaskenv'."""
    path_to_base_dir = Path(__file__).parent.parent.parent
    path_to_env_file = os.path.join(path_to_base_dir, '.flaskenv')
    load_dotenv(path_to_env_file)
    apy_id = os.environ.get('APY_ID')
    return apy_id
