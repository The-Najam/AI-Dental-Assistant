import sqlite3
from config.setting import setting
from config.logger import logger
import os

def database_connection():
    try:
        if not setting.database_path.exists():
            raise FileNotFoundError("Database Path is Not found")
        os.makedirs(os.path.dirname(setting.database_path), exist_ok=True)
        db_connection = sqlite3.connect(setting.database_path)
        cursor = db_connection.cursor()
        logger.info("Database Connection is Successfully Created")
        return db_connection, cursor
    except Exception as e:
        logger.exception("Failed to connect to database")
        raise ConnectionError(f"Failed To Connect Database : {e}") from e



def table_creation(db_connection, cursor):
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS LEADS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    question TEXT,
                    message TEXT,
                    timestamp INTEGER)""")
        db_connection.commit()
        db_connection.close()
        logger.info("Table Is Sucessfully Created!")
    except sqlite3.Error:
        db_connection.rollback()
        logger.exception("Table creation failed")
        raise




def delete_db(db_connection, cursor):
    try:
        cursor.execute("""DELETE FROM LEADS""")
        db_connection.commit()
        db_connection.close()
    except sqlite3.Error:
        db_connection.rollback()
        logger.exception("Table deletion failed")
        raise




if __name__ == "__main__":
    try:
        db_connection, cursor = database_connection()
        table_creation(db_connection, cursor)
    except Exception:
        logger.exception("Database setup failed")
        raise
