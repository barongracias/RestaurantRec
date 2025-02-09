# imports
import os
import googlemaps
import time
import sqlite3

# project imports
from src.logger import get_console_logger
logger = get_console_logger(name='api_request')

# SQLite setup for storing data
def setup_db():
    conn = sqlite3.connect('restaurants.db')
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

# Insert data into the SQLite database
def insert_data_to_db(cursor, data):
    logger.info('Inserting data into database...')
    for restaurant in data:
        cursor.execute('''
        INSERT OR REPLACE INTO restaurants (id, name, price_level, rating, num_reviews, neighbourhood)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (restaurant['place_id'], restaurant['name'], restaurant.get('price_level'), restaurant.get('rating'), restaurant.get('user_ratings_total'), restaurant['tag']))
    cursor.connection.commit()

# pull API key from env
try:
    api_key = os.environ['GOOGLE_API_KEY']
except KeyError:
    logger.error('Google API key environemnt variable not set')
    raise

# connect to googlemaps client
gmaps = googlemaps.Client(key=api_key)

# pick neighborhoods
neighborhoods = ['Soho', 'Shoreditch', 'Covent Garden', 'Camden',
                 'Mayfair', 'Kensington', 'Paddington', 'Fitzrovia',
                 'Borough', 'London City', 'Holborn', 'South Bank',
                 'Elephant and Castle', 'Chinatown', 'Notting Hill',
                 'Westminster', 'Chelsea', 'Southwark', 'Southbank',
                 'Waterloo', 'Kings Cross', 'Marylebone', 'Angel']

cuisines = ['traditional', 'mexican', 'latin', 'burger', 'pizza',
            'high cuisine', 'american', 'italian', 'turkish',
            'mediterranean', 'chinese', 'asian', 'indian', 'japanese',
            'british', 'persian', 'european', 'pub', 'thai', 'sushi',
            'spanish', 'steak', 'pizza']

# list to store all restaurant data
restaurants = []

# function to parse the API response
def restaurant_response(response_items, tag):
    restaurant_responses = []
    for item in response_items:
        item_dict = {}
        item_dict['tag'], item_dict['name'], item_dict['place_id'], item_dict['price_level'], item_dict['rating'], item_dict['user_ratings_total'] = tag, item.get('name'), item.get('place_id'), item.get('price_level'), item.get('rating'), item.get('user_ratings_total')
        restaurant_responses.append(item_dict)
    return restaurant_responses
    
# Fetch and store restaurant data for each neighborhood and cuisine
def fetch_restaurant_data():
    conn, cursor = setup_db()  # Initialize database connection and cursor
    
    # Step 1: Collect restaurant data for each neighborhood
    for neighborhood in neighborhoods:
        query_neighborhood = neighborhood + " London"
        place = gmaps.geocode(query_neighborhood)
        if place:
            place_info = place[0]
            geo_results = place_info['geometry']
            geo_coordinates = geo_results['location']
            lat = geo_coordinates['lat']
            lng = geo_coordinates['lng']

            flag = False
            counter = 0
            while not flag:
                if counter == 0:
                    results = gmaps.places(type="restaurant", location=[lat, lng], radius=3000)
                    response_items = results['results']
                    restaurants_data = restaurant_response(response_items, neighborhood)
                    restaurants.extend(restaurants_data)
                    counter += 1
                else:
                    if results.get('next_page_token') is None:
                        flag = True
                    else:
                        next_page = results.get('next_page_token')
                        time.sleep(2)
                        results = gmaps.places(type="restaurant", location=[lat, lng], radius=2000, page_token=next_page)
                        response_items = results['results']
                        restaurants_data = restaurant_response(response_items, neighborhood)
                        restaurants.extend(restaurants_data)
                        counter += 1

    # Step 2: Collect restaurant data for each cuisine type
    for cuisine in cuisines:
        flag = False
        counter = 0
        while not flag:
            if counter == 0:
                results = gmaps.places(query=f"{cuisine} restaurants in London", type="restaurant", location=[lat, lng], radius=3000)
                response_items = results['results']
                restaurants.extend(restaurant_response(response_items, cuisine))
                counter += 1
            else:
                if results.get('next_page_token') is None:
                    flag = True
                else:
                    next_page = results.get('next_page_token')
                    time.sleep(2)
                    results = gmaps.places(query=f"{cuisine} restaurants in London", type="restaurant", location=[lat, lng], radius=3000, page_token=next_page)
                    response_items = results['results']
                    restaurants.extend(restaurant_response(response_items, cuisine))
                    counter += 1
    
    # insert the fetched restaurant data into the database
    logger.info('Connecting to database...')
    insert_data_to_db(cursor, restaurants)
    
    # get database row count
    cursor.execute('SELECT COUNT(*) FROM restaurants')
    rows = cursor.fetchall()
    logger.info(f"{str(rows[0]).replace('(','').replace(')','').replace(',','')} rows inserted into restaurant database")
    
    # close connection
    logger.info('Committing and closing connection...')
    conn.close()
    logger.info('Restaurants data has been inserted into the database...')

if __name__ == '__main__':
    # call the function to fetch and store data
    fetch_restaurant_data()