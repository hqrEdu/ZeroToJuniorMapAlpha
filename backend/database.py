import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error


class Database:
    def __init__(self, database, user, password, host):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=5432)
        self.cur = self.conn.cursor()

    def get_users(self):
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """SELECT u.discord, c.city_name, u.stack, c.lat, c.lng
                    FROM user_data u JOIN city c ON u.city_id = c.city_id;"""
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
        except Error:
            return 503
        else:
            return result  
        finally:
            self._close()  

    def add_user(self, discord, city_name, stack):
        query = """INSERT INTO user_data (discord, city_id, stack) VALUES
                   (%(discord)s, (SELECT city_id FROM city WHERE city_name = %(city_name)s), %(stack)s);"""
        try:
            self.cur.execute(query, ({"discord": discord, "city_name": city_name, "stack": stack}))
            self.conn.commit()
            return 201
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return 409
        except Error:
            self.conn.rollback()
            return 503
        finally:
            self._close()

    def update_user_name(self, old_discord, new_discord):
        query = "UPDATE user_data SET discord = %(new_discord)s WHERE discord = %(old_discord)s;"
        try:
            self.cur.execute(query, ({"new_discord": new_discord, "old_discord": old_discord}))
            self.conn.commit()
            return 204
        except Error:
            self.conn.rollback()
            return 503
        finally:
            self._close()

    def update_user_city(self, discord, city_id):
        query = "UPDATE user_data SET city_id = %(city_id)s WHERE discord = %(discord)s;"
        try:
            self.cur.execute(query, ({"city_id": city_id, "discord": discord}))
            self.conn.commit()
            return 204
        except Error:
            return 503
        finally:
            self._close()
        
    def update_user_stack(self, discord, stack):
        query = "UPDATE user_data SET stack = %(stack)s WHERE discord = %(discord)s;"
        try:
            self.cur.execute(query, ({"stack": stack, "discord": discord}))
            self.conn.commit()
            return 204
        except Error:
            return 503
        finally:
            self._close()

    def delete_user(self, discord):
        query = "DELETE FROM user_data WHERE discord = %(discord)s;"
        try:
            self.cur.execute(query, ({"discord": discord}))
            self.conn.commit()
            return 204
        except Error:
            return 503
        finally:
            self._close()
        
    def user_exists(self, discord):
        query = "SELECT discord FROM user_data WHERE discord = %(discord)s;"
        self.cur.execute(query, ({"discord": discord}))
        return True if self.cur.fetchone() else False

    def select_user_city_id(self, discord):
        query = "SELECT city_id from user_data WHERE discord = %(discord)s;"
        self.cur.execute(query, ({"discord": discord}))
        user_city_id = self.cur.fetchone()[0]
        return user_city_id
    
    def select_user_stack(self, discord):
        query = "SELECT stack FROM user_data WHERE discord = %(discord)s"
        self.cur.execute(query, ({"discord": discord}))
        user_stack = self.cur.fetchone()[0]
        return user_stack

    def select_city_id(self, city_name):
        query = "SELECT city_id FROM city WHERE city_name = %(city_name)s;"
        self.cur.execute(query, ({"city_name": city_name}))
        city_id = self.cur.fetchone()[0]
        return city_id
    
    def city_exists(self, city_name):
        query = "SELECT city_name FROM city WHERE city_name = %(city_name)s"
        self.cur.execute(query, ({"city_name": city_name}))
        return True if self.cur.fetchone() else False

    def add_city(self, city_name, latitude, longitude):
        query = "INSERT INTO city (city_name, lat, lng) VALUES (%(city_name)s, %(latitude)s, %(longitude)s);"
        self.cur.execute(query, ({"city_name": city_name, "latitude": latitude, "longitude": longitude}))
        self.conn.commit()

    def _close(self):
        self.cur.close()
        self.conn.close()