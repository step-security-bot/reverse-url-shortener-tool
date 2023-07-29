import concurrent.futures
from time import sleep

class URLManager:

    def __init__(self, url):
        self.url = url
        # Lista de tuplas (id, path, status_code, redirect_url)
        self.urls_redirect = []
        # Executor
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def start(self):

        while True:
            self.url.current_path = "".join([self.url.path_characters[position] for position in self.url.permutation_notation])
            self.url.current_id += 1
            self.send_task(self.url.current_id, self.url.current_path)
            # Encontrar el siguiente índice a incrementar
            index = self.url.path_length - 1 # Se resta 1 para usarlo como índice de lista
            # Mientras los números a la derecha sean los máximos, moverse a la izquierda
            while index >= 0 and self.url.permutation_notation[index] == len(self.url.path_characters) - 1:
                index -= 1
            # Si todos los índices han alcanzado el máximo, terminar el bucle
            if index < 0:
                break
            # Incrementar el índice / posición
            self.url.permutation_notation[index] += 1
            # Ajustar los siguientes índices de la derecha a 0
            for position in range(index + 1, self.url.path_length):
                self.url.permutation_notation[position] = 0
                    
    def send_task(self, current_id, current_path):
        """Envía una tarea al `executor` y libera recursos cada 200 peticiones"""
        if current_id % 200 == 0 and current_id:
            print("Wait...\n")
            sleep(10)
            print(self.urls_redirect)
            self.urls_redirect = []
        # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible
        self.executor.submit(self.url.get_redirect_url, current_id, current_path, self)
