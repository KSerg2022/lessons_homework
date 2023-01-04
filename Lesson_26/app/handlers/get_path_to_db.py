"""Ger path to database."""
import os
from pathlib import Path
from dotenv import load_dotenv

import web


def get_path_to_db():
    """Get path to database"""
    path_to_base_dir = Path(web.__file__).parent
    path_to_env_file = os.path.join(path_to_base_dir, '.flaskenv')
    load_dotenv(path_to_env_file)
    db_name = os.environ.get('DATABASE')
    path_to_db = os.path.join(path_to_base_dir, db_name)
    return path_to_db
