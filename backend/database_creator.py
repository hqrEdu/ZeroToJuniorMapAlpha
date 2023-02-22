import psycopg2

user = "postgres"
password = "password"
host = "localhost"
port = 5432

# CREATE Z2J DATABASE
conn = psycopg2.connect(user=user, password=password, host=host, port=port)
conn.autocommit = True
cur = conn.cursor()
query = """SELECT 'CREATE DATABASE z2j_map' 
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'z2j_map')"""
cur.execute(query)
conn.close()

# CONNECT TO DATABASE

database = "z2j_map"

conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# CREATE TABLES

query = """CREATE TABLE city (
            city_id SERIAL PRIMARY KEY,
            city_name VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT
        );

        CREATE TABLE USER_DATA (
            username VARCHAR(255) UNIQUE,
            city_id INT REFERENCES city(city_id),
            field VARCHAR(255) 
        );"""

cur.execute(query)
conn.commit()

