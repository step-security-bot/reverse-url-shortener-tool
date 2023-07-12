# controller/shorturl_controller.property

from model.shorturl_model import ShortURLModel

class ShortURLController:
    def __init__(self, domain, domain_length, characters):
        self.model = ShortURLModel(domain, domain_length, characters)

    def generate_short_url(self) -> None:
        self.model.start_process()

# db/database.py

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

# model/shorturl_model.py

import concurrent.futures
from db.database import Database
from utils.shorturl_utils import get_url_available

class ShortURLModel:
    def __init__(self, domain, domain_length, characters):
        self.database = Database()
        self.response_list = None
        self.id_state = None
        self.domain = domain
        self.domain_length = domain_length
        self.characters = characters

    def start_process(self) -> None:
        self.response_list = []
        
        num_characters = len(self.characters)

        # Recuperar la lista de índices de la base de datos

        indices = self.load_state()
        print(f"Retomando ejecución desde {indices}\n")


        # Executor
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

        # Generar las permutaciones iterativamente
        futures = []
        iter = 0
        while True:
            iter += 1
            # Permutación actual usando el arreglo de índices y la lista de caracteres
            path = "".join([self.characters[i] for i in indices])

            if iter > 1: # TODO: Ignorar el primer elemento
                # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible
                try:
                    futures.append(executor.submit(get_url_available, self.domain, path, iter, self))
                except:
                    executor.shutdown(cancel_futures=True)
                    self.save_state()
                    break

            # Encontrar el siguiente índice a incrementar
            i = self.domain_length - 1

            # Mientras los números a la derecha sean los máximos, moverse a la izquierda
            while i >= 0 and indices[i] == num_characters - 1:
                i -= 1

            # Si todos los índices han alcanzado el máximo, terminar el bucle
            if i < 0:
                break

            # Incrementar el índice encontrado y ajustar los siguientes índices de la derecha a 0
            indices[i] += 1

            for j in range(i + 1, self.domain_length):
                indices[j] = 0

        # Cerrar el executor después de terminar el procesamiento
        executor.shutdown()

    def save_state(self) -> None:
        if self.response_list:
            self.database.insert_data(self.response_list)
        else:
            print("\nExiting...", end="")

    def load_state(self) -> list:
        self.database.cursor.execute("SELECT COUNT(*) FROM base_1")
        result = self.database.cursor.fetchone()

        if result[0] > 0:
            self.database.cursor.execute("SELECT id FROM base_1 ORDER BY code DESC LIMIT 1")
            result = self.database.cursor.fetchone()
            id_state = result[0]
            # Retorna una lista de los índices de los caracteres
            return [self.characters.index(i) for i in id_state]
        else:
            index = [0] * self.domain_length
            id_state = ''.join(self.characters[i] for i in index)

            return index

    def id_exist(self, id: str) -> bool:
        self.database.cursor.execute("SELECT EXISTS(SELECT id FROM base_1 WHERE id=%s);", (id,))
        return self.database.cursor.fetchone()[0]

# utils/shorturl_utils.py

import requests

def get_url_available(domain, path, code, model):
    try:
        url = domain + path
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        status_code = response.status_code

        if (
            response.history
            and response.url != domain
            and path != model.id_state
        ):
            result = response.url[8:]
            if path != model.id_state:
                print(f"({status_code}) {url} -> https://{result}\n")
                model.response_list.append((path, status_code, result, code))

    except requests.exceptions.RequestException as e:
        print(f"\nError ({url}):", e)


# view/shorturl_view.py

class ShortURLView:
    def __init__(self, controller):
        self.controller = controller

    def start(self, domain_option):
        self.controller.generate_short_url()
 
 # main.py

from argparse import ArgumentParser
from string import ascii_letters, digits

from controller.shorturl_controller import ShortURLController
from view.shorturl_view import ShortURLView

def main():
    CHARACTERS = ascii_letters + digits
    SHORTURL_DOMAINS = {
        1: ["https://t.ly/", 4],
        2: ["https://rb.gy/", 5],
        3: ["https://www.shorturl.at/", 5],
        4: ["https://tinyurl.com/", 6],
    }

    # Configurar el análisis de argumentos
    parser = ArgumentParser()
    parser.add_argument("-d", "--domain_option", type=int, help="Opción de dominio (1-4)")
    args = parser.parse_args()

    # Obtener la opción de dominio del argumento
    domain_option = args.domain_option

    # Verificar si se proporcionó la opción de dominio
    if domain_option is None:
        parser.error("Debe proporcionar una opción de dominio (-d / --domain_option)")
    
    if domain_option not in SHORTURL_DOMAINS:
        parser.error("Opción de dominio inválida")
    
    domain = SHORTURL_DOMAINS[domain_option][0]
    domain_length = SHORTURL_DOMAINS[domain_option][1]

    controller = ShortURLController(domain, domain_length, CHARACTERS) # Domain option, para globalizar
    view = ShortURLView(controller)
    
    view.start(domain_option)


if __name__ == "__main__":
    main()
