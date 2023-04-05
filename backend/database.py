import psycopg2
from psycopg2.extras import RealDictCursor
from utility_functions.api_exceptions import InternalServerError, BadRequest

class Database:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    database=self.database,
                    user=self.user, 
                    password=self.password, 
                    host=self.host, 
                    port=self.port
                    )
                self.conn.autocommit = True
                self.cur = self.conn.cursor() 
            except psycopg2.DatabaseError as e:
                raise InternalServerError
        return self.conn

        
    def get_all(self, query):
        self.conn = self.connect()
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            self.cur = self.conn.cursor()
            return result
        except Exception:
            raise InternalServerError  
        
    def get_cell(self, query, values):
        self.conn = self.connect()
        self.cur.execute(query, (values))
        try:
            cell_value = self.cur.fetchone()[0]
            return cell_value
        except:
            return False
        
    def run_query(self, query, values):
        self.conn = self.connect()
        try:
            self.cur.execute(query, (values))
            row_count = self.cur.rowcount
            if row_count == 0:
                raise BadRequest
            else:
                self.conn.commit()
                return row_count
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            raise BadRequest(detail="Entered discord username already exists in the database.")
        except Exception:
            self.conn.rollback()
            raise InternalServerError
