import psycopg2
from psycopg2.extensions import AsIs as asis


############################################

# the whole script executes after creating the class object and using the "check_database()" method 

#############################################



class DatabaseCreator:

    database = "z2j_map"
    user_data_table = "user_data"
    cities_table = "cities"
    postcodes_table = "postcodes"
    discord_column = "discord"
    city_id_column = "city_id"
    postcode_id_column = "postcode_id"
    stack_column = "stack"
    city_name_column = "city_name"
    postcode_column = "postcode"
    latitude_column = "lat"
    longitude_column = "lng"

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = self.database
        self.expected_tables = {self.user_data_table, self.cities_table, self.postcodes_table}
        self.expected_user_data_columns = {self.discord_column, self.city_id_column, self.postcode_id_column, self.stack_column}
        self.expected_cities_columns = {self.city_id_column, self.city_name_column}
        self.expected_postcodes_columns = {self.postcode_id_column, self.postcode_column, self.city_id_column, self.latitude_column, self.longitude_column}

    def _connect_to_server(self):
        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password)
        self.cur = self.conn.cursor()
    
    def _connect_to_database(self):
        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
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
            %s VARCHAR(255)
        );

        CREATE TABLE %s (
            %s SERIAL PRIMARY KEY,
            %s VARCHAR(20) UNIQUE,
            %s INT REFERENCES %s(%s),
            %s FLOAT,
            %s FLOAT
        );

        CREATE TABLE %s (
            %s VARCHAR(255) UNIQUE,
            %s INT REFERENCES %s(%s),
            %s INT REFERENCES %s(%s),
            %s VARCHAR(255) 
        );"""
        self.cur.execute(query, (asis(self.cities_table), asis(self.city_id_column), asis(self.city_name_column),
                                    asis(self.postcodes_table), asis(self.postcode_id_column), asis(self.postcode_column), asis(self.city_id_column),
                                    asis(self.cities_table), asis(self.city_id_column), asis(self.latitude_column), 
                                    asis(self.longitude_column),
                                    asis(self.user_data_table), asis(self.discord_column), asis(self.city_id_column),
                                    asis(self.cities_table), asis(self.city_id_column), asis(self.postcode_id_column),
                                    asis(self.postcodes_table), asis(self.postcode_id_column), asis(self.stack_column)))
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
        self.cur.execute(query, (self.user_data_table,))
        for column in self.cur.fetchall():
            current_columns.add(column[0])

        if current_columns != self.expected_user_data_columns:
            return False
        else:
            return True

    def _check_cities_columns(self):
        current_columns = set()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
        self.cur.execute(query, (self.cities_table,))

        for column in self.cur.fetchall():
            current_columns.add(column[0])

        if current_columns != self.expected_cities_columns:
            return False
        else:
            return True
        
    def _check_postcodes_columns(self):
        current_columns = set()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
        self.cur.execute(query, (self.postcodes_table,))

        for column in self.cur.fetchall():
            current_columns.add(column[0])

        if current_columns != self.expected_postcodes_columns:
            return False
        else:
            return True


    def get_proper_database(self):
        self._connect_to_server()
        self._create_database_if_not_exists()
        self._connect_to_database()
        if not all([self._check_tables(), self._check_user_data_columns(), self._check_cities_columns(),
                        self._check_postcodes_columns()]):
            self._remake_tables()
        self._close()



dc = DatabaseCreator(user="postgres", password="superuser", host="localhost", port=5432)

dc.get_proper_database()