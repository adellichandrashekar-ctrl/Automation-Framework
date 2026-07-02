import sqlite3
import logging

logger = logging.getLogger(__name__)

class DBHelper:
    def __init__(self, db_name="automation_test.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        logger.info(f"Connected to Database: {self.db_name}")
        return self.conn

    def execute_query(self, query, params=()):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        logger.info(f"Executed Query: {query}")

    def fetch_all(self, query, params=()):
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
