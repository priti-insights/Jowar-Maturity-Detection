
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "jowarai_db"),
    )

    if connection.is_connected():
        print("MySQL connection successful!")

        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        print("Tables:", cursor.fetchall())

        cursor.close()
        connection.close()

except mysql.connector.Error as error:
    print("MySQL connection failed:", error)
