import sqlite3

import click
import mysql.connector
from decouple import config as getenv


class Database:
    def __init__(self):
        self.table_name = "urls"
        if getenv("APP_SERVICE_DEBUG") == "true":
            self.conn = sqlite3.connect(
                "./service/data_generator_service/database/my_database.db"
            )
        else:
            click.echo("Starting...")
            self.conn = mysql.connector.connect(
                host=getenv("DB_HOST", "127.0.0.1"),
                port=getenv("DB_PORT", "3306"),
                database=getenv("DB_DATABASE", "forge"),
                user=getenv("DB_USERNAME", "forge"),
                password=getenv("DB_PASSWORD", ""),
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
            )

        if self.conn.is_connected():
            click.echo("Conexión exitosa a la base de datos MySQL.")

        self.cursor = self.conn.cursor()

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
        else:
            # Para MySQL (marcador de posición '%s')
            self.cursor.executemany(
                f"""
                INSERT INTO {self.table_name} (id, path, status_code, redirect_url)
                VALUES (%s, %s, %s, %s)
                """,
                data,
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
