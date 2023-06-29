from flask import Flask, redirect, request
import string, os, pickle
from time import sleep
import concurrent.futures, requests

CHARACTERS = string.ascii_letters + string.digits
PRODUCTION = os.getenv("PRODUCTION")

SHORTURL_DOMAINS = {
    "https://t.ly/": 4,
    "https://shorturl.lol/": 4,
    "https://rb.gy/": 5,
    "https://www.shorturl.at/": 5,
    "https://tinyurl.com/": 6,
}

app = Flask(__name__)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

def start_process(characters: str, domain_option: int) -> None:
    global indices
    num_characters = len(characters)

    # Cargar la longitud del dominio y el dominio a usar
    domain_length = list(SHORTURL_DOMAINS.values())[domain_option]
    domain = list(SHORTURL_DOMAINS.keys())[domain_option]

    # Recuperar la lista de índices
    if os.path.exists(f"./state_{domain_option}.pkl"):
        indices = load_state(f"./state_{domain_option}.pkl")
        print("Retomando ejecución\n")
    else:
        # Lista de índices base
        indices = [0] * domain_length

    # Generar las permutaciones iterativamente
    futures = []
    iter = int()
    while True:
        iter += 1
        # Permutación actual usando el arreglo de índices y la lista de caracteres
        path = "".join([characters[i] for i in indices])

        # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible
        futures.append(executor.submit(get_url_available, domain, path))

        # Cada 20 iteraciones, se verifica los resultados
        if iter % 20 == 0:
            get_url_available("https://meyer-s-store.vercel.app/", "top-secret")
            # Iterar sobre cada futuro completado en la lista de futuros
            for future in concurrent.futures.as_completed(futures):
                # Obtener el resultado del futuro completado
                result = future.result()

                # Si el resultado no es None (es decir, se encontró una URL corta), imprimirlo en la consola
                if result is not None:
                    print(result)
            futures = []

        # Encontrar el siguiente índice a incrementar
        i = domain_length - 1

        # Mientras los números a la derecha sean los máximos, moverse a la izquierda
        while i >= 0 and indices[i] == num_characters - 1:
            i -= 1

        # Si todos los índices han alcanzado el máximo, terminar el bucle
        if i < 0:
            break

        # Incrementar el índice encontrado y ajustar los siguientes índices de la derecha a 0
        indices[i] += 1

        for j in range(i + 1, domain_length):
            indices[j] = 0

    # Cerrar el executor después de terminar el procesamiento
    executor.shutdown()

def get_url_available(domain, path):
    """Comprueba si una URL corta está disponible."""
    try:
        url = domain + path

        response = requests.get(url, timeout=10)

        response.encoding = "utf-8"

        if response.history and response.url != domain:
            return f"{url} -> {response.url}\n"

    except requests.exceptions.RequestException:
        pass

    return None

# Función para guardar el estado en un archivo
def save_state(filename: str, data) -> None:
    try:
        with open(filename, "wb") as file:
            pickle.dump(data, file)
    except IOError:
        print(f"Error: No se pudo guardar el estado en el archivo {filename}")

# Función para cargar el estado desde un archivo
def load_state(filename: str):
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: Archivo {filename} no encontrado")
    except IOError:
        print(f"Error: No se pudo leer del archivo {filename}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def redirect_to_specific_url(path):
    global domain_option

    if PRODUCTION:
        domain_option = 1
        executor.submit(start_process, CHARACTERS, domain_option)
    else:
        # Seleccionar un dominio
        counter = 1

        for key in SHORTURL_DOMAINS.keys():
            print(f"{counter}. {key}")
            counter += 1

        domain_option = int(input("\nIngrese una opción (1 - 5): ")) - 1
        print()

        start_process(CHARACTERS, domain_option)

    return "Proceso de recolección de URLs iniciado"

if __name__ == "__main__":
    try:
        app.run()
    except:
        try:
            # Guardar el estado en un archivo
            save_state(f"state_{domain_option}.pkl", indices)
            print("\n\nEstado de ejecución guardado")
        except:
            print("\n\nError")

