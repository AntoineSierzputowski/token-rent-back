import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLDB:
    def __init__(self):
        self._conn = None
        self._config = {
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "database": os.getenv("DB_NAME", "token_rent_back"),
            "port": int(os.getenv("DB_PORT", 3306))
        }

    def get_connection(self):
        if self._conn is None or not self._conn.is_connected():
            try:
                self._conn = mysql.connector.connect(**self._config)
            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                     temp_config = self._config.copy()
                     del temp_config["database"]
                     temp_conn = mysql.connector.connect(**temp_config)
                     cursor = temp_conn.cursor()
                     cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self._config['database']}")
                     temp_conn.close()
                     self._conn = mysql.connector.connect(**self._config)
                else:
                    raise err
        return self._conn

    def init_db(self):
        """Initialize the database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                last_name VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                date_of_birth DATE NOT NULL,
                salary FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()

db = MySQLDB()
