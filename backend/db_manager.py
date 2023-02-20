import psycopg2
from psycopg2.extras import RealDictCursor
import json


class DatabaseManager:
    def __init__(self, database, user, password, host, port):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def get_users(self):
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """SELECT u.username, c.city_name, u.field, c.latitude, c.longitude
                    FROM user_data u JOIN city c ON u.city_id = c.city_id;"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.cur = self.conn.cursor()
        return json.dumps(result, ensure_ascii=False).encode("utf-8")

    def add_user(self, username, city_name, field, latitude, longitude):
        self.city_exists(city_name, latitude, longitude)
        query = """INSERT INTO user_data (username, city_id, field)
                    SELECT %s, city_id, %s FROM city WHERE city_name = %s;"""
        try:
            self.cur.execute(query, (username, field, city_name))
            self.conn.commit()
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return json.dumps({"success": False, "message": "User already exists."})

        return json.dumps({"success": True, "message": "Sign up successful."})
    
    def edit_user_name(self, username, new_username):
        query = "UPDATE user_data SET username = %s WHERE username = %s"
        self.cur.execute(query, (new_username, username))
        self.conn.commit()
        return json.dumps({"success": True, "message": "Username has been changed succesfully."})
    
    def edit_user_city(self, username, city_name, latitude, longitude):
        self.city_exists(city_name, latitude, longitude)
        query = "SELECT city_id FROM city WHERE city_name = %s;"
        self.cur.execute(query, (city_name,))
        city_id = self.cur.fetchone()
        query = "UPDATE user_data SET city_id = %s WHERE username = %s;"
        self.cur.execute(query, (city_id, username))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User city has been changed succesfully."})
    
    def edit_user_field(self, username, field):
        query = "UPDATE user_data SET field = %s WHERE username = %s"
        self.cur.execute(query, (field, username))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User field has been changed succesfully."})

    def delete_user(self, username):
        query = "DELETE FROM user_data WHERE username = %s"
        self.cur.execute(query, (username,))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User deleted successfully."})

    def close_connection(self):
        self.conn.close()

    def city_exists(self, city_name, latitude, longitude):
        query = "SELECT city_name FROM city WHERE city_name = %s"
        self.cur.execute(query, (city_name,))
        exist = self.cur.fetchone() is not None
        if not exist:
            query = "INSERT INTO city (city_name, latitude, longitude) VALUES (%s, %s, %s);"
            self.cur.execute(query, (city_name, latitude, longitude))
            self.conn.commit()

db = DatabaseManager("z2j_map", "postgres", "superuser", "localhost", 5432)
