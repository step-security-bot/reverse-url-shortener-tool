# ./components/url/url_manager.py
import concurrent.futures
from time import sleep

from database.database_connection import Database


class URLManager:
    def __init__(self, url, database):
        self.url = url
        self.database = database
        # Lista de tuplas (id, path, status_code, redirect_url)
        self.urls_redirect = []
        # Executor
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def start(self):
        self.set_current_url_data_notation()

        while True:
            self.url.current_path = "".join(
                [
                    self.url.path_characters[position]
                    for position in self.url.current_permutation_notation
                ]
            )
            self.url.current_id += 1
            self.send_task(self.url.current_id, self.url.current_path)

            self.generate_next_permutation()

    def send_task(self, current_id, current_path):
        """Libera recursos cuando se encuentre mínimo 20 peticiones"""
        if len(self.urls_redirect) % 10 == 0 and self.urls_redirect:
            self.save_data()
        # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible
        self.executor.submit(self.url.get_redirect_url, current_id, current_path, self)

    def add_url_data(self, url_data):
        self.urls_redirect.append(url_data)

    def set_current_url_data_notation(self):
        if self.database.is_not_empty():
            self.url.current_path = self.database.get_last_path_by_id()
            self.url.current_id = self.database.get_last_id()
            # Lista de los índices de los caracteres
            self.url.current_permutation_notation = [
                self.url.path_characters.index(character)
                for character in self.url.current_path
            ]
            # Paso a la siguiente url, ya que la actual ya está en la base de datos
            self.generate_next_permutation()
        else:
            self.url.current_permutation_notation = [0] * self.url.path_length

    def save_data(self):
        # print("Espera...\n")
        sleep(10)
        data = self.urls_redirect
        self.database.insert_data(data)
        self.urls_redirect.clear()

    def generate_next_permutation(self):
        # Encontrar el siguiente índice a incrementar
        index = self.url.path_length - 1  # Se resta 1 para usarlo como índice de lista
        # Mientras los números a la derecha sean los máximos, moverse a la izquierda
        while (
            index >= 0
            and self.url.current_permutation_notation[index]
            == len(self.url.path_characters) - 1
        ):
            index -= 1
        # Si todos los índices han alcanzado el máximo, terminar el bucle
        if index < 0:
            self.save_data()
            exit()
        # Incrementar el índice / posición
        self.url.current_permutation_notation[index] += 1
        # Ajustar los siguientes índices de la derecha a 0
        for position in range(index + 1, self.url.path_length):
            self.url.current_permutation_notation[position] = 0


# ./components/url/url.py
import requests

from utils.constants import CHARACTERS


class URL:
    def __init__(self, domain: str, path_length: int):
        self.domain = domain
        self.path_length = path_length
        self.path_characters: str = CHARACTERS
        self.current_path: str = None
        self.current_id: int = 0

        self.current_permutation_notation = []
        self.number_of_path_permutations: int = (
            len(self.path_characters) ** self.path_length
        )

    def get_redirect_url(self, id: int, path: str, url_manager):
        url = f"https://{self.domain}/{path}"

        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"\nError ({url}):", e)
            return

        response.encoding = "utf-8"
        status_code = response.status_code

        if response.history and response.url != self.domain:
            redirect_url = response.url[8:]
            # print(f"{id}. ({status_code}) {url} -> https://{redirect_url}\n")
            url_manager.add_url_data((id, path, status_code, redirect_url))


# ./main.py
from components.url.url import URL
from components.url.url_manager import URLManager
from database.database_connection import Database
from utils.constants import SHORTURL_DOMAINS


def main():
    global url_manager
    database = Database()

    domain_option = 1
    domain = SHORTURL_DOMAINS[domain_option][0]
    path_length = SHORTURL_DOMAINS[domain_option][1]

    url = URL(domain, path_length)
    url_manager = URLManager(url, database)

    url_manager.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("#" * 94, "executor.shutdown(cancel_futures=True)\n")
        url_manager.executor.shutdown(cancel_futures=True)
        print("*" * 94, "database.conn.close()")
        url_manager.database.conn.close()
        print("&" * 94, "Done!")
        exit()

# ./utils/constants.py
from string import ascii_letters, digits

CHARACTERS = ascii_letters + digits

SHORTURL_DOMAINS = {
    1: ["t.ly", 4],
    2: ["rb.gy", 5],
    3: ["www.shorturl.at", 5],
    4: ["tinyurl.com", 6],
}

# ./database/database_connection.py
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
