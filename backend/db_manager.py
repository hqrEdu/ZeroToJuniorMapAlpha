import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
import json


class DatabaseManager:
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
            self.cur = self.conn.cursor()
        except Error as error:
            return json.dumps({"success": False, "message": error.pgerror})
        else:
            return json.dumps(result, ensure_ascii=False).encode("utf-8")

    def add_user(self, discord, city_name, stack, lat, lng):
        self._city_exists(city_name, lat, lng)
        query = """INSERT INTO user_data (discord, city_id, stack) VALUES
                   (%s, (SELECT city_id FROM city WHERE city_name = %s), %s);"""
        try:
            self.cur.execute(query, (discord, city_name, stack))
            self.conn.commit()
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return json.dumps({"success": False, "message": "User already exists."})
        except Error as error:
            self.conn.rollback()
            return json.dumps({"success": False, "message": error.pgerror})
        else:
            return json.dumps({"success": True, "message": "Sign up successful."})

    def edit(self, **kwargs):   ### You need to provide which argument you pass, eg (discord = "username", city_name = "Warsaw")
       
        def edit_user_name(discord, new_discord):
            query = "UPDATE user_data SET discord = %s WHERE discord = %s"
            self.cur.execute(query, (new_discord, discord))
            self.conn.commit()
            return "name"
    
        def edit_user_city(discord, city_name, lat, lng):
            self._city_exists(city_name, lat, lng)
            query = "SELECT city_id FROM city WHERE city_name = %s;"
            self.cur.execute(query, (city_name,))
            city_id = self.cur.fetchone()
            query = "UPDATE user_data SET city_id = %s WHERE discord = %s;"
            self.cur.execute(query, (city_id, discord))
            self.conn.commit()
            return "city"
        
        def edit_user_stack(discord, stack):
            query = "UPDATE user_data SET stack = %s WHERE discord = %s"
            self.cur.execute(query, (stack, discord))
            self.conn.commit()
            return "stack"

        discord = kwargs.get("discord")
        new_discord = kwargs.get("new_discord")
        city_name = kwargs.get("city_name")
        lat = kwargs.get("lat")
        lng = kwargs.get("lng")
        stack = kwargs.get("stack")

        user_in_data = self._user_exists(discord)
        
        if not kwargs:
            return json.dumps({"success": False, "message": "There is no data to be changed"})
        if not user_in_data:
            return json.dumps({"success": False, "message": "This user does not exist."})
        
        changed = []
        if new_discord:
            changed.append(edit_user_name(discord, new_discord))
        if city_name and lat and lng:
            changed.append(edit_user_city(discord, city_name, lat, lng))
        if stack:
            changed.append(edit_user_stack(discord, stack))

        if len(changed) == 0:
            return json.dumps({"success": False, "message": "Not enough information"})
        elif len(changed) == 1:
            return json.dumps({"success": True, "message": f"User {changed[0]} has been changed."})
        else:
            return json.dumps({"success": True, "message": f"User {', '.join(changed)} have been changed."})
        

    def delete_user(self, discord):
        user_in_data = self._user_exists(discord)
        if not user_in_data:
            return json.dumps({"success": False, "message": "This user does not exist."})
        query = "DELETE FROM user_data WHERE discord = %s"
        self.cur.execute(query, (discord,))
        self.conn.commit()
        return json.dumps({"success": True, "message": "User deleted successfully."})

    def close_connection(self):
        self.conn.close()

    def _user_exists(self, username):
        query = "SELECT discord FROM user_data WHERE discord = %s"
        self.cur.execute(query, (username,))
        user_in_data = True if self.cur.fetchone() else False
        return user_in_data
    
    def _city_exists(self, city_name, lat, lng):

        def add_city(city_name, latitude, longitude):
            query = "INSERT INTO city (city_name, lat, lng) VALUES (%s, %s, %s);"
            self.cur.execute(query, (city_name, latitude, longitude))
            self.conn.commit()

        query = "SELECT city_name FROM city WHERE city_name = %s"
        self.cur.execute(query, (city_name,))
        exist = self.cur.fetchone()
        if not exist:
            add_city(city_name, lat, lng)

db = DatabaseManager(database="z2j_map", user="postgres", password="superuser", host="localhost")


print(db.edit(discord="Andrzej", city_name="Warsaw", lng=21211.221))
