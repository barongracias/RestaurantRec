import sqlite3
import pandas as pd

conn = sqlite3.connect('restaurants.db')
df = pd.read_sql_query("SELECT * FROM restaurants", conn)
conn.close()

print(df[df['neighbourhood'] == 'Soho'].sort_values(by=['rating', 'num_reviews'], ascending=False))

# print(df[df['neighbourhood'] == 'Soho'].size)