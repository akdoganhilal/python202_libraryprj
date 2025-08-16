import sqlite3

class Database:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        self.close()

db = Database()
db.create_table()