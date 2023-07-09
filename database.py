import psycopg2
from decouple import config as getenv

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            user=getenv("user"),
            password=getenv("password"),
            host=getenv("host"),
            port=getenv("port"),
            database=getenv("database"),
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS base_1 (
                id VARCHAR(10) PRIMARY KEY NOT NULL,
                redirect_url TEXT,
                status_code INTEGER,
                code INTEGER,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

        self.conn.commit()

    def insert_data(self, data):

        print("\nSaving state...", end="")
        self.conn.rollback()

        self.cursor.executemany(
            """
            INSERT INTO base_1 (id, status_code, redirect_url, code)
            VALUES (%s, %s, %s, %s)
            """,
            data,
        )

        self.conn.commit()
        print("Done!")
