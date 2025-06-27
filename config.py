# config.py
import mysql.connector
import os
from mysql.connector import errorcode

def get_db_connection():
    try:
        print("Trying to connect to DB with:")
        print("HOST:", os.environ.get("MYSQLHOST"))
        print("USER:", os.environ.get("MYSQLUSER"))
        print("DB:", os.environ.get("MYSQLDATABASE"))

        conn = mysql.connector.connect(
            host=os.environ.get("MYSQLHOST"),
            user=os.environ.get("MYSQLUSER"),
            password=os.environ.get("MYSQLPASSWORD"),
            database=os.environ.get("MYSQLDATABASE"),
            port=int(os.environ.get("MYSQLPORT", 3306))
        )
        return conn
    except mysql.connector.Error as err:
        print("ERROR CODE:", err.errno)
        print("MESSAGE:", err.msg)
        print("SQLSTATE:", err.sqlstate)
        raise
