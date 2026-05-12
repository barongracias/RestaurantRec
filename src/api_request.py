import os
import time
import sqlite3

import googlemaps

from src.logger import get_console_logger
from src.paths import DB_PATH

logger = get_console_logger(name='api_request')

NEIGHBORHOODS = [
    'Soho', 'Shoreditch', 'Covent Garden', 'Camden',
    'Mayfair', 'Kensington', 'Paddington', 'Fitzrovia',
    'Borough', 'London City', 'Holborn', 'South Bank',
    'Elephant and Castle', 'Chinatown', 'Notting Hill',
    'Westminster', 'Chelsea', 'Southwark', 'Southbank',
    'Waterloo', 'Kings Cross', 'Marylebone', 'Angel',
]

CUISINES = [
    'traditional', 'mexican', 'latin', 'burger', 'pizza',
    'high cuisine', 'american', 'italian', 'turkish',
    'mediterranean', 'chinese', 'asian', 'indian', 'japanese',
    'british', 'persian', 'european', 'pub', 'thai', 'sushi',
    'spanish', 'steak',
]

LONDON_CENTER = (51.5074, -0.1278)


def setup_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    logger.info('Creating or checking for existing database...')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id TEXT PRIMARY KEY,
            name TEXT,
            price_level INTEGER,
            rating REAL,
            num_reviews INTEGER,
            neighbourhood TEXT
        )
    ''')
    conn.commit()
    return conn, cursor


def parse_results(results, tag):
    rows = []
    for item in results:
        rows.append({
            'tag': tag,
            'name': item.get('name'),
            'place_id': item.get('place_id'),
            'price_level': item.get('price_level'),
            'rating': item.get('rating'),
            'user_ratings_total': item.get('user_ratings_total'),
        })
    return rows


def insert_restaurants(conn, cursor, restaurants):
    logger.info('Inserting %d records into database...', len(restaurants))
    cursor.executemany(
        '''
        INSERT OR REPLACE INTO restaurants
            (id, name, price_level, rating, num_reviews, neighbourhood)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        [
            (r['place_id'], r['name'], r.get('price_level'),
             r.get('rating'), r.get('user_ratings_total'), r['tag'])
            for r in restaurants
        ],
    )
    conn.commit()


def paginate(gmaps, **kwargs):
    """Yield all result pages for a gmaps.places() call."""
    response = gmaps.places(**kwargs)
    yield response.get('results', [])
    while response.get('next_page_token'):
        time.sleep(2)
        response = gmaps.places(page_token=response['next_page_token'])
        yield response.get('results', [])


def fetch_restaurant_data():
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        logger.error('GOOGLE_API_KEY environment variable is not set.')
        raise SystemExit(1)

    gmaps = googlemaps.Client(key=api_key)
    conn, cursor = setup_db(DB_PATH)
    restaurants = []

    for neighborhood in NEIGHBORHOODS:
        geocode = gmaps.geocode(f'{neighborhood} London')
        if geocode:
            loc = geocode[0]['geometry']['location']
            lat, lng = loc['lat'], loc['lng']
        else:
            logger.warning('Could not geocode %s; using London centre.', neighborhood)
            lat, lng = LONDON_CENTER

        for page in paginate(gmaps, type='restaurant', location=(lat, lng), radius=3000):
            restaurants.extend(parse_results(page, neighborhood))

    for cuisine in CUISINES:
        lat, lng = LONDON_CENTER
        for page in paginate(
            gmaps,
            query=f'{cuisine} restaurants in London',
            type='restaurant',
            location=(lat, lng),
            radius=3000,
        ):
            restaurants.extend(parse_results(page, cuisine))

    insert_restaurants(conn, cursor, restaurants)

    cursor.execute('SELECT COUNT(*) FROM restaurants')
    count = cursor.fetchone()[0]
    logger.info('%d rows in restaurant database.', count)

    conn.close()
    logger.info('Done.')


if __name__ == '__main__':
    fetch_restaurant_data()
