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
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        
    def get_all(self, query):
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        except Exception as error:
            raise error  
        
    def get_cell(self, query, values):
        self.cur.execute(query, (values))
        try:
            cell_value = self.cur.fetchone()[0]
            return cell_value
        except:
            return False
        
    def run_query(self, query, values):
        try:
            self.cur.execute(query, (values))
            row_count = self.cur.rowcount
            if row_count == 0:
                raise ValueError
            else:
                self.conn.commit()
                return row_count
        except Exception as error:
            self.conn.rollback()
            raise error
        
    def disconnect(self):
        self.cur.close()
        self.conn.close()