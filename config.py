import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='yamabiko.proxy.rlwy.net',
            port=35892,
            user='root',
            password='abcd1234',  # 🔁 Replace with your actual password
            database='railway'
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("DB authentication error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError("DB does not exist")
        else:
            raise
