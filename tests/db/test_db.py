import pytest
import logging
from utils.db_helper import DBHelper

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def db():
    database = DBHelper("test_users.db")
    database.execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
       )
    ''')

    yield database

    database.execute_query("DROP TABLE users")
    database.close()

@pytest.mark.db
class TestDatabaseOperations:
    
    def test_insert_and_verify_user(self, db):
        logger.info("Inserting user into DB...")
        db.execute_query("INSERT INTO users (name, role) VALUES (?, ?)",
                         ("Chandra Shekar", "Automation Engineer"))
        
        logger.info("Fetching users from DB...")
        results = db.fetch_all("SELECT * FROM users WHERE name = ?", ("Chandra Shekar",))
        logger.info(f"The result/ data from DB is {results}")
        assert len(results) == 1, "Expected exactly 1 user to be returned"
        assert results[0][1] == "Chandra Shekar"
        assert results[0][2] == "Automation Engineer"
        logger.info("Database insertion and verification successful")
