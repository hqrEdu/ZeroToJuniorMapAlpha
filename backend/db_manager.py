import psycopg2
from psycopg2.extras import RealDictCursor
import json


class DatabaseManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def close(self):
        self.conn.close()

    def insert_user(self, username, city, *field):
        cursor = self.conn.cursor()
        try:
            if field:
                query = "INSERT INTO user_data (username, city, field) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, city, field))
            else:
                query = "INSERT INTO user_data (username, city) VALUES (%s, %s)"
                cursor.execute(query, (username, city))
            self.conn.commit()
            return json.dumps({"success": True, "message": "Sign up successful."})
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return json.dumps({"success": False, "message": "User already exists."})
        except:
            return json.dumps({"success": False, "message": "Inserting the user into the database failed."})

    def get_all(self):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT username, city, field FROM user_data"
        cursor.execute(query)
        result = cursor.fetchall()
        return json.dumps(result)



    
