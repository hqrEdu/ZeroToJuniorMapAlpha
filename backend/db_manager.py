import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error


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
        except Error as error:
            return {"success": False, "message": error.pgerror}
        else:
            return {"success": True, "message": result}   ###   result can be convert to json object 

    def add_user(self, discord, city_name, stack):
        query = """INSERT INTO user_data (discord, city_id, stack) VALUES
                   (%s, (SELECT city_id FROM city WHERE city_name = %s), %s);"""
        try:
            self.cur.execute(query, (discord, city_name, stack))
            self.conn.commit()
            return {"success": True, "message": "Sign up successful."}
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return {"success": False, "message": "User already exists."}
        except Error as error:
            self.conn.rollback()
            return {"success": False, "message": error.pgerror}

    def update_user_name(self, old_discord, new_discord):
        query = "UPDATE user_data SET discord = %s WHERE discord = %s;"
        try:
            self.cur.execute(query, (new_discord, old_discord))
            self.conn.commit()
            return {"success": True, "message": "User name has been changed."}
        except Error as error:
            self.conn.rollback()
            return {"success": False, "message": error.pgerror}

    def update_user_city(self, discord, city_id):
        query = "UPDATE user_data SET city_id = %s WHERE discord = %s;"
        try:
            self.cur.execute(query, (city_id, discord))
            self.conn.commit()
            return {"success": True, "message": "User city has been updated."}
        except Error as error:
            return {"success": False, "message": error.pgerror}

    def update_user_stack(self, discord, stack):
        query = "UPDATE user_data SET stack = %s WHERE discord = %s;"
        try:
            self.cur.execute(query, (stack, discord))
            self.conn.commit()
            return {"success": True, "message": "User stack has been updated."}
        except Error as error:
            return {"success": False, "message": error.pgerror}

    def delete_user(self, discord):
        query = "DELETE FROM user_data WHERE discord = %s;"
        try:
            self.cur.execute(query, (discord,))
            self.conn.commit()
            return {"success": True, "message": "User deleted successfully."}
        except Error as error:
            return {"success": False, "message": error.pgerror}
        
    def user_exists(self, username):
        query = "SELECT discord FROM user_data WHERE discord = %s;"
        self.cur.execute(query, (username,))
        return True if self.cur.fetchone() else False

    def select_city_id(self, city_name):
        query = "SELECT city_id FROM city WHERE city_name = %s;"
        self.cur.execute(query, (city_name,))
        city_id = self.cur.fetchone()[0]
        return city_id
    
    def city_exists(self, city_name):
        query = "SELECT city_name FROM city WHERE city_name = %s"
        self.cur.execute(query, (city_name,))
        return True if self.cur.fetchone() else False

    def add_city(self, city_name, latitude, longitude):
        query = "INSERT INTO city (city_name, lat, lng) VALUES (%s, %s, %s);"
        self.cur.execute(query, (city_name, latitude, longitude))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()



