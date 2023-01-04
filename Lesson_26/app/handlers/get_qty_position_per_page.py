"""Get quantity position per page for pagination."""
from pathlib import Path
import os
from dotenv import load_dotenv


def get_qty_position_per_page():
    """Get quantity position per page from '.flaskenv'."""
    path_to_base_dir = Path(__file__).parent.parent.parent
    path_to_env_file = path_to_base_dir / '.flaskenv'
    load_dotenv(path_to_env_file)
    qty_per_page = os.environ.get('QTY_PER_PAGE')
    return int(qty_per_page)
