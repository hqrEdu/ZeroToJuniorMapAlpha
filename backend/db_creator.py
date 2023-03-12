import psycopg2
from psycopg2.extensions import AsIs as asis


############################################

# the whole script executes after creating the class object and using the "check_database()" method 

#############################################



class DatabaseCreator:

    city = "city"
    user_data = "user_data"
    discord = "discord"
    city_id = "city_id"
    stack = "stack"
    city_name = "city_name"
    latitude = "lat"
    longitude = "lng"
    database = "z2j_map"

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.database = self.database
        self.expected_tables = {self.city, self.user_data}
        self.expected_user_data_columns = {self.discord, self.city_id, self.stack}
        self.expected_city_columns = {self.city_id, self.city_name, self.latitude, self.longitude}

    def _connect_to_server(self):
        self.conn = psycopg2.connect(host=self.host, user=self.user, password=self.password)
        self.cur = self.conn.cursor()
    
    def _connect_to_database(self):
        self.conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cur = self.conn.cursor()

    def _close(self):
        self.cur.close()
        self.conn.close()

    def _remake_tables(self):
        self._remove_tables()
        self._create_tables()

    def _remove_tables(self):
        self.cur.execute("DROP SCHEMA public CASCADE;")
        self.cur.execute("CREATE SCHEMA public;")
        self.conn.commit()

    def _create_tables(self):
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
        self.cur.execute(query, (asis(self.city), asis(self.city_id), 
                                asis(self.city_name), asis(self.latitude), asis(self.longitude), asis(self.user_data),
                                asis(self.discord), asis(self.city_id), asis(self.city), asis(self.city_id), asis(self.stack)))
        self.conn.commit()

    def _create_database_if_not_exists(self):
        self.conn.autocommit = True
        query = "CREATE DATABASE %s;"
        try:
            self.cur.execute(query, (asis(self.database),))
        except psycopg2.errors.DuplicateDatabase:
            pass

    def _check_tables(self):
        current_tables = set()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
        self.cur.execute(query)

        for table in self.cur.fetchall():
            current_tables.add(table[0])
        if current_tables != self.expected_tables:
            return False
        else:
            return True

    def _check_user_data_columns(self):
        current_columns = set()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
        self.cur.execute(query, (self.user_data,))
        for column in self.cur.fetchall():
            current_columns.add(column[0])

        if current_columns != self.expected_user_data_columns:
            return False
        else:
            return True

    def _check_city_columns(self):
        current_columns = set()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
        self.cur.execute(query, (self.city,))

        for column in self.cur.fetchall():
            current_columns.add(column[0])

        if current_columns != self.expected_city_columns:
            return False
        else:
            return True

    def check_database(self):
        self._connect_to_server()
        self._create_database_if_not_exists()
        self._connect_to_database()
        if not all([self._check_tables(), self._check_user_data_columns(), self._check_city_columns()]):
            self._remake_tables()
        self._close()

dcc = DatabaseCreator(host="localhost", user="postgres", password="superuser")
dcc.check_database()

