import psycopg2
from psycopg2.extensions import AsIs as asis


#### LOGIN

host = "host"
user = "user"
password = "password"

#### CAN BE CHANGED
database = "z2j_map"
city = "city"
user_data = "user_data"
discord = "discord"
city_id = "city_id"
stack = "stack"
city_name = "city_name"
latitude = "lat"
longitude = "lng"


expected_tables = {city, user_data}
expected_user_data_columns = {discord, city_id, stack}
expected_city_columns = {city_id, city_name, latitude, longitude}


def remake_tables():
    def remove_tables():
        cur.execute("DROP SCHEMA public CASCADE;")
        cur.execute("CREATE SCHEMA public;")
        conn.commit()
    def create_tables():
        query = """CREATE TABLE %s (
            %s SERIAL PRIMARY KEY,
            %s VARCHAR(255),
            %s FLOAT,
            %s FLOAT
        );

        CREATE TABLE %s (
            %s VARCHAR(255) UNIQUE,
            %s INT REFERENCES %s(%s),
            %s VARCHAR(255) 
        );"""
        cur.execute(query, (asis(city), asis(city_id), asis(city_name), asis(latitude), asis(longitude), asis(user_data),
                            asis(discord), asis(city_id), asis(city), asis(city_id), asis(stack)))
        conn.commit()
    
    remove_tables()
    create_tables()


conn = psycopg2.connect(host=host, user=user, password=password)
cur = conn.cursor()


####  CHECK IF DATABASE EXISTS, CREATE IF NOT 
conn.autocommit = True
query = "CREATE DATABASE %s;"
try:
    cur.execute(query, (asis(database),))
except psycopg2.errors.DuplicateDatabase:
    pass
conn.close()

#### CONNECT TO DATABASE
conn = psycopg2.connect(host=host, user=user, password=password, database=database)
cur = conn.cursor()

# CHECK TABLES NAME

current_tables = set()
query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
cur.execute(query)

for table in cur.fetchall():
    current_tables.add(table[0])

if current_tables != expected_tables:
    remake_tables()
    

# ### CHECK COLUMNS NAME IN USER_DATA TABLE

current_columns = set()
query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
cur.execute(query, (user_data,))

for column in cur.fetchall():
    current_columns.add(column)

if current_columns != expected_user_data_columns:
    remake_tables()

### CHECK COLUMNS NAME IN CITY TABLE

current_columns = set()
query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
cur.execute(query, (city,))

for column in cur.fetchall():
    current_columns.add(column)

if current_columns != expected_user_data_columns:
    remake_tables()

