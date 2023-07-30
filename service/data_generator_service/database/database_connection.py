import psycopg2
import sqlite3
from decouple import config as getenv


class Database:
    def __init__(self):
        self.table_name = "url_data"
        if getenv("APP_DEBUG") == "true":
            self.conn = sqlite3.connect(
                "./service/data_generator_service/database/my_database.db"
            )
        else:
            self.conn = psycopg2.connect(
                host=getenv("DB_HOST"),
                port=getenv("DB_PORT"),
                database=getenv("DB_DATABASE"),
                user=getenv("DB_USERNAME"),
                password=getenv("DB_PASSWORD"),
            )

        self.cursor = self.conn.cursor()

        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY NOT NULL,
                path VARCHAR(10),
                status_code INTEGER,
                redirect_url TEXT,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

        self.conn.commit()

    def insert_data(self, data: list[tuple]):
        print("\nGuardando datos...", end=" ")
        self.conn.rollback()

        if isinstance(self.conn, sqlite3.Connection):
            # Para SQLite (marcador de posición '?')
            self.cursor.executemany(
                f"""
                INSERT INTO {self.table_name} (id, path, status_code, redirect_url)
                VALUES (?, ?, ?, ?)
                """,
                data,
            )
        elif isinstance(self.conn, psycopg2.extensions.connection):
            # Para PostgreSQL (marcador de posición '%s')
            self.cursor.executemany(
                f"""
                INSERT INTO {self.table_name} (id, path, status_code, redirect_url)
                VALUES (%s, %s, %s, %s)
                """,
                data,
            )
        else:
            raise ValueError(
                "Tipo de conexión desconocido. No se puede determinar el tipo de marcador de posición."
            )

        self.conn.commit()
        print("Done!\n")

    def is_not_empty(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        result = self.cursor.fetchone()

        return True if result[0] > 0 else False

    def get_last_path_by_id(self):
        self.cursor.execute(
            f"SELECT path FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        )
        result = self.cursor.fetchone()

        return result[0]

    def get_last_id(self):
        self.cursor.execute(
            f"SELECT id FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        )
        result = self.cursor.fetchone()

        return result[0]
