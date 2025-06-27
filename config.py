# config.py
import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='yamabiko.proxy.rlwy.net',      # Railway host
            port=35892,                           # Railway port
            user='root',                          # Railway username
            password='YOUR_RAILWAY_PASSWORD',     # Click "show" on Railway and paste here
            database='railway'                    # Default Railway DB name
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("DB authentication error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError("Database does not exist")
        else:
            raise
