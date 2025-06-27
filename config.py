# config.py
import mysql.connector
import os
from mysql.connector import errorcode

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("MYSQLHOST", "railway"),
            user=os.environ.get("MYSQLUSER", "root"),
            password=os.environ.get("MYSQLPASSWORD", "EWQFpxAkmIsLhvSNPvIOtVynRtXWYPXM"),
            database=os.environ.get("MYSQLDATABASE", "railway"),
            port=int(os.environ.get("MYSQLPORT", 3306))
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("DB authentication error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError("Database does not exist")
        else:
            raise
