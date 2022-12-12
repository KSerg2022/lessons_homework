"""Get quantity position per page for pagination"""
from pathlib import Path
import os
from dotenv import load_dotenv

import web


def get_qty_position_per_page():
    """Get quantity position per page from '.flaskenv'"""
    path_to_base_dir = Path(web.__file__).parent
    path_to_env_file = os.path.join(path_to_base_dir, '.flaskenv')
    load_dotenv(path_to_env_file)
    qty_per_page = os.environ.get('QTY_PER_PAGE')
    return int(qty_per_page)
