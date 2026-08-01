import sqlite3
from config.setting import setting
from config.logger import logger
import smtplib
from email.message import EmailMessage
import os
import resend


def database_connection():
    try:
        os.makedirs(os.path.dirname(setting.database_path), exist_ok=True)
        db_connection = sqlite3.connect(setting.database_path)
        cursor = db_connection.cursor()
        logger.info("Database Connection is Successfully Created")
    except Exception as e:
        logger.critical("Database Connection Failed")

    return db_connection, cursor



def table_creation(db_connection, cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS LEADS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                question TEXT,
                message TEXT,
                timestamp INTEGER)""")
    db_connection.commit()
    logger.info("Table Is Sucessfully Created!")

def delete_db(db_connection, cursor):
    cursor.execute("""DELETE FROM LEADS""")
    db_connection.commit()


def notifier(name,email,question,message):
    recipient_email = setting.client_email
    resend.api_key = setting.resend_api_key
   
    params: resend.Emails.SendParams = {
    "from": "onboarding@resend.dev",
    "to": [recipient_email],
    "subject": "New lead captured from your website chatbot",
    "html": f"""
    <p><strong>New lead from your website chatbot:</strong></p>
    <p>Name: {name}<br>
    Email: {email}<br>
    Question: {question}<br>
    Additional message: {message or 'N/A'}</p>
    """,
    }
    try:
        resend.Emails.send(params)
        logger.info("Notification send Successfully!")
    except Exception as e:
        logger.error(f"Sending Email Failed! : {e}")



if __name__ == "__main__":
    try:
        db_connection = sqlite3.connect(setting.database_path)
        cursor = db_connection.cursor()
        logger.info("Database Connection is Successfully Created")
    except Exception as e:
        logger.critical("Database Connection Failed")
    table_creation(db_connection, cursor)

