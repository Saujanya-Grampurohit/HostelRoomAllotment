# config.py
import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root@123',           # your MySQL password
            database='hostel_allotment'
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("DB auth error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError("DB does not exist")
        else:
            raise
