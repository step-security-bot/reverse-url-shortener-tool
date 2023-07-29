import concurrent.futures
from time import sleep

class URLManager:

    def __init__(self, url):
        self.url = url
        self.urls_redirect = []
        # Executor
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def start(self):
        permutation_list = [0] * self.url.path_length

        while True:
            self.url.set_current_path_by_permutation_notation(permutation_list)
            self.send_task(self.url.current_path)
            # Encontrar el siguiente índice a incrementar
            index = self.url.path_length - 1 # Se resta 1 para usarlo como índice de lista
            # Mientras los números a la derecha sean los máximos, moverse a la izquierda
            while index >= 0 and permutation_list[index] == len(self.url.path_characters) - 1:
                index -= 1
            # Si todos los índices han alcanzado el máximo, terminar el bucle
            if index < 0:
                break
            # Incrementar el índice / posición
            permutation_list[index] += 1
            # Ajustar los siguientes índices de la derecha a 0
            for position in range(index + 1, self.url.path_length):
                permutation_list[position] = 0
                    
    def send_task(self, path):
        if self.url.current_id % 200 == 0:
            print("Wait...\n")
            # TODO: Guardar urls obtenidas
            sleep(10)
        # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible
        self.executor.submit(self.url.get_redirect_url, path)
