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
