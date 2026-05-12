import sqlite3
import pandas as pd

from src.paths import DB_PATH
from src.logger import get_console_logger

logger = get_console_logger(name='data')


def load_restaurants():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query('SELECT * FROM restaurants', conn)
    except Exception:
        logger.error('Database not found or table missing. Run `python -m src.api_request` first.')
        df = pd.DataFrame()
    finally:
        conn.close()
    return df


if __name__ == '__main__':
    df = load_restaurants()
    if not df.empty:
        print(df[df['neighbourhood'] == 'Soho'].sort_values(
            by=['rating', 'num_reviews'], ascending=False
        ))
