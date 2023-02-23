import psycopg2

host = "host"
user = "user"
password = "password"

# CREATE Z2J DATABASE
# conn = psycopg2.connect(server=server, user=user, password=password)
# conn.autocommit = True
# cur = conn.cursor()
# query = """SELECT 'CREATE DATABASE z2j_map' 
#         WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'z2j_map')"""
# cur.execute(query)
# conn.close()

# CONNECT TO DATABASE

database = "database"

conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cur = conn.cursor()

# CREATE TABLES

query = """CREATE TABLE city (
            city_id SERIAL PRIMARY KEY,
            city_name VARCHAR(255),
            lat FLOAT,
            lng FLOAT
        );

        CREATE TABLE USER_DATA (
            discord VARCHAR(255) UNIQUE,
            city_id INT REFERENCES city(city_id),
            stack VARCHAR(255) 
        );"""

cur.execute(query)
conn.commit()
conn.close()
