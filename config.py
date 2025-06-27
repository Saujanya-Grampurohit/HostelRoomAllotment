# config.py
import os
import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    try:
        # Print statements for debug (Render logs)
        print("🔧 Connecting to MySQL with:")
        print("HOST:", os.environ.get('MYSQLHOST'))
        print("PORT:", os.environ.get('MYSQLPORT'))
        print("USER:", os.environ.get('MYSQLUSER'))
        print("DATABASE:", os.environ.get('MYSQLDATABASE'))

        conn = mysql.connector.connect(
            host=os.environ.get('MYSQLHOST'),
            port=int(os.environ.get('MYSQLPORT', 3306)),
            user=os.environ.get('MYSQLUSER'),
            password=os.environ.get('MYSQLPASSWORD'),
            database=os.environ.get('MYSQLDATABASE')
        )
        print("✅ Database connection successful.")
        return conn

    except mysql.connector.Error as err:
        print("❌ Database connection failed.")
        print("ERROR CODE:", err.errno)
        print("MESSAGE:", err.msg)
        print("SQLSTATE:", err.sqlstate)
        
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError("DB authentication error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise RuntimeError("Database does not exist")
        else:
            raise RuntimeError("DB connection error") from err
