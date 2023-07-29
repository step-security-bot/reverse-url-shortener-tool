import concurrent.futures
from time import sleep

from db.database import Database
from utils.shorturl_utils import get_url_available
from utils.constants import CHARACTERS

class ShortURLModel:
    def __init__(self, domain, domain_length):
        self.database = Database()
        self.response_list = []
        self.id_state = None
        self.domain = domain
        self.domain_length = domain_length
        self.path = None
        self.characters = CHARACTERS
        # Executor
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def start_process(self) -> None:
        # Recuperar el último índices de la base de datos
        indices = self.load_state()
        print(f"Retomando ejecución desde {indices}\n")

        # Generar las permutaciones iterativamente
        iter = 0
        while True:
            iter += 1

            try:
                self.check_iter(iter)
            except Exception as e:
                print(f"Model: {e}")

            # Permutación actual usando el arreglo de índices y la lista de caracteres
            self.path = "".join([self.characters[i] for i in indices])

            try:
                self.send_task(iter)
            except Exception as e:
                print(f"Model: {e}")

            # Encontrar el siguiente índice a incrementar
            index = self.domain_length - 1

            # Mientras los números a la derecha sean los máximos, moverse a la izquierda
            while index >= 0 and indices[index] == len(self.characters) - 1:
                index -= 1

            # Si todos los índices han alcanzado el máximo, terminar el bucle
            if index < 0:
                break

            # Incrementar el índice encontrado y ajustar los siguientes índices de la derecha a 0
            indices[index] += 1

            for j in range(index + 1, self.domain_length):
                indices[j] = 0

        self.executor.shutdown()

    def save_state(self) -> None:
        data = self.response_list
        self.response_list.clear()
        self.database.insert_data(data)
        self.executor.shutdown(cancel_futures=True)
        exit()

    def load_state(self) -> list:
        self.database.cursor.execute("SELECT COUNT(*) FROM base_1")
        result = self.database.cursor.fetchone()

        if result[0] > 0:
            self.database.cursor.execute("SELECT id FROM base_1 ORDER BY code DESC LIMIT 1")
            result = self.database.cursor.fetchone()
            self.id_state = result[0]
            # Retorna una lista de los índices de los caracteres
            return [self.characters.index(i) for i in self.id_state]
        else:
            index = [0] * self.domain_length
            self.id_state = ''.join(self.characters[i] for i in index)

            return index

    def id_exist(self, id: str) -> bool:
        self.database.cursor.execute("SELECT EXISTS(SELECT id FROM base_1 WHERE id=%s);", (id,))
        return self.database.cursor.fetchone()[0]

    def send_task(self, iter):
        if iter > 1: # TODO: Ignorar el primer elemento
            # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible
            try:
                self.executor.submit(get_url_available, self.domain, self.path, self)
            except Exception as e:
                print(e)
                self.save_state()

    def check_iter(self, iter):
        if iter % 200 == 0:
            print(f"Última id de tarea: {iter} ... liberando recursos")
            sleep(10)
        if len(self.response_list) > 20:
            data = self.response_list
            self.response_list.clear()
            print(f"Tareas completadas: {len(data)}.")
            self.database.insert_data(data)