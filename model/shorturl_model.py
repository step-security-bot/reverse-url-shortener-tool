import concurrent.futures
from database import Database
from utils import get_url_available

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
