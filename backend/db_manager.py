import psycopg2
from psycopg2.extras import RealDictCursor
import json


class DatabaseManager:
    def __init__(self, database, user, password, host):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=5432)
        self.cur = self.conn.cursor()

    def get_users(self):
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """SELECT u.discord, c.city_name, u.stack, c.lat, c.lng
                    FROM user_data u JOIN city c ON u.city_id = c.city_id;"""
        self.cur.execute(query)
        result = self.cur.fetchall()
        self.cur = self.conn.cursor()
        return json.dumps(result, ensure_ascii=False).encode("utf-8")

    def add_user(self, discord, city_name, stack, lat, lng):
        exist = self.city_exists(city_name)
        if not exist:
            self.add_city(city_name, lat, lng)
        query = """INSERT INTO user_data (discord, city_id, stack) VALUES
                   (%s, (SELECT city_id FROM city WHERE city_name = %s), %s);"""
        try:
            self.cur.execute(query, (discord, city_name, stack))
            self.conn.commit()
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return json.dumps({"success": False, "message": "User already exists."})

        return json.dumps({"success": True, "message": "Sign up successful."})
    
    def edit_user_name(self, discord, new_discord):
        query = "UPDATE user_data SET discord = %s WHERE discord = %s"
        self.cur.execute(query, (new_discord, discord))
        self.conn.commit()
        return json.dumps({"success": True, "message": "discord has been changed succesfully."})
    
    def edit_user_city(self, discord, city_name, lat, lng):
        exist = self.city_exists(city_name)
        if not exist:
            self.add_city(city_name, lat, lng)
        query = "SELECT city_id FROM city WHERE city_name = %s;"
        self.cur.execute(query, (city_name,))
        city_id = self.cur.fetchone()
        query = "UPDATE user_data SET city_id = %s WHERE discord = %s;"
        self.cur.execute(query, (city_id, discord))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User city has been changed succesfully."})
    
    def edit_user_stack(self, discord, stack):
        query = "UPDATE user_data SET stack = %s WHERE discord = %s"
        self.cur.execute(query, (stack, discord))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User stack has been changed succesfully."})

    def delete_user(self, discord):
        query = "DELETE FROM user_data WHERE discord = %s"
        self.cur.execute(query, (discord,))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User deleted successfully."})

    def close_connection(self):
        self.conn.close()

    def city_exists(self, city_name):
        query = "SELECT city_name FROM city WHERE city_name = %s"
        self.cur.execute(query, (city_name,))
        exist = self.cur.fetchone() is not None
        return exist
    
    def add_city(self, city_name, lat, lng):
        query = "INSERT INTO city (city_name, lat, lng) VALUES (%s, %s, %s);"
        self.cur.execute(query, (city_name, lat, lng))
        self.conn.commit()

