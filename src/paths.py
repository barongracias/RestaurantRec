from pathlib import Path

PARENT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PARENT_DIR / 'data'
DB_PATH = PARENT_DIR / 'restaurants.db'

DATA_DIR.mkdir(exist_ok=True)
