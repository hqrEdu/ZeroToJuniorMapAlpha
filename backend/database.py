import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self, database, user, password, host):
        self.database = database
        self.user = user
        self.password = password
        self.host = host

    def connect(self):
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host)
        self.cur = self.conn.cursor()
        
    def handle_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                row_count = args[0].cur.rowcount
                if row_count == 0:
                    raise ValueError
                args[0].conn.commit()
                return row_count
            except Exception as error:
                args[0].conn.rollback()
                raise error
        return wrapper

    def get_users(self):
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """SELECT u.discord, c.city_name, u.stack, c.lat, c.lng
                    FROM user_data u JOIN city c ON u.city_id = c.city_id;"""
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        except Exception as error:
            raise error  
        
    @handle_exceptions
    def add_user(self, discord, city_name, stack):
        query = """INSERT INTO user_data (discord, city_id, stack) VALUES
                   (%(discord)s, (SELECT city_id FROM city WHERE city_name = %(city_name)s), %(stack)s);"""
        self.cur.execute(query, ({"discord": discord, "city_name": city_name, "stack": stack}))

    @handle_exceptions
    def update_user(self, kwargs):
        discord = kwargs.get("discord")
        new_discord = kwargs.get("new_discord")
        city_id = kwargs.get("city_id")
        stack = kwargs.get("stack")
        
        query = "UPDATE user_data SET "
        if new_discord:
            query += f"discord = '{new_discord}', "
        if city_id:
            query += f"city_id = '{city_id}', "
        if stack:
            query += f"stack = '{stack}', "

        query = query[:-2] + " WHERE discord = %(discord)s"
        self.cur.execute(query, ({"discord": discord}))

    @handle_exceptions
    def delete_user(self, discord):
        query = "DELETE FROM user_data WHERE discord = %(discord)s;"
        self.cur.execute(query, ({"discord": discord}))

    @handle_exceptions
    def add_city(self, city_name, latitude, longitude):
        query = "INSERT INTO city (city_name, lat, lng) VALUES (%(city_name)s, %(latitude)s, %(longitude)s);"
        try:
            self.cur.execute(query, ({"city_name": city_name, "latitude": latitude, "longitude": longitude}))
            self.conn.commit()
        except Exception as error:
            self.conn.rollback()
            raise error
    
    def select_city_id(self, city_name):
        query = "SELECT city_id FROM city WHERE city_name = %(city_name)s;"
        self.cur.execute(query, ({"city_name": city_name}))
        city_id = self.cur.fetchone()[0]
        return city_id
    
    def city_exists(self, city_name):
        query = "SELECT city_name FROM city WHERE city_name = %(city_name)s"
        self.cur.execute(query, ({"city_name": city_name}))
        return True if self.cur.fetchone() else False
        
    def disconnect(self):
        self.cur.close()
        self.conn.close()