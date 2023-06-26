import string
import os
import pickle
from time import sleep
import concurrent.futures
import random
import requests
import asyncio

# Definir caracteres válidos para las permutaciones
CARACTERES = string.ascii_letters + string.digits

# Definir los dominios de URL corta a utilizar y su longitud 
DOMINIOS_URL_CORTA = {
    "https://t.ly/": 4,
    "https://shorturl.lol/": 4,
    "https://rb.gy/": 5,
    "https://www.shorturl.at/": 5,
    "https://tinyurl.com/": 6,
}

# Variable global para almacenar los índices actuales de la permutación 
indices = []

async def iniciar_proceso(characters: str, opcion_dominio: int) -> None:
    global indices
    
    # Obtener longitud del dominio y el dominio a usar según la opción seleccionada 
    longitud_dominio = list(DOMINIOS_URL_CORTA.values())[opcion_dominio]
    dominio = list(DOMINIOS_URL_CORTA.keys())[opcion_dominio]
    
    # Recuperar la lista de índices si existe un archivo de estado previo 
    if os.path.exists(f"./state_{opcion_dominio}.pkl"):
        indices = cargar_estado(f"./state_{opcion_dominio}.pkl")
        print("Retomando ejecución\n")
    else:
        # Crear una lista de índices base 
        indices = [0] * longitud_dominio
    
    # Crear un executor para enviar solicitudes de verificación de URL en paralelo 
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        
        # Generar las permutaciones iterativamente 
        while True:
            # Obtener la permutación actual usando los índices y la lista de caracteres
            ruta = "".join([characters[i] for i in indices])

            # Crear una lista vacía para almacenar las tareas que se enviarán al executor 
            tareas = []

            # Enviar una tarea al executor para verificar si la URL corta formada por el dominio y la ruta está disponible 
            tareas.append(loop.run_in_executor(executor, get_url_disponible, dominio, ruta))

            # Esperar a que se completen todas las tareas enviadas al executor
            resultados = await asyncio.gather(*tareas)

            # Loop over each completed future (i.e. task) in the list of futures
            for resultado in resultados:
                # Si el resultado no es None (es decir, se encontró una URL corta disponible), imprimirlo en la consola 
                if resultado is not None:
                    print(resultado)

            # Encontrar el siguiente índice a incrementar 
            i = longitud_dominio - 1
            
            # Mientras los números a la derecha sean los máximos, moverse a la izquierda
            while i >= 0 and indices[i] == len(characters) - 1:
                i -= 1

            # Si todos los índices han alcanzado el máximo, terminar el bucle 
            if i < 0:
                break

            # Incrementar el índice encontrado y ajustar los siguientes índices de la derecha a 0 
            indices[i] += 1
            for j in range(i + 1, longitud_dominio):
                indices[j] = 0
    
    # Guardar el estado en un archivo después de terminar el procesamiento 
    guardar_estado(f"state_{opcion_dominio}.pkl", indices)
    print("\n\nEstado de ejecución guardado")

def get_url_disponible(dominio, ruta):
    """Verificar si una URL corta está disponible."""
    try:
        url = dominio + ruta
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        if response.history and response.url != dominio:
            return f"{url} -> {response.url}\n"
    except requests.exceptions.RequestException:
        pass
    return None

# Función para guardar el estado en un archivo 
def guardar_estado(nombre_archivo: str, datos) -> None:
    try:
        with open(nombre_archivo, "wb") as archivo:
            pickle.dump(datos, archivo)
    except IOError:
        print(f"Error: No se pudo guardar el estado en el archivo {nombre_archivo}")

# Función para cargar el estado desde un archivo 
def cargar_estado(nombre_archivo: str):
    try:
        with open(nombre_archivo, "rb") as archivo:
            datos = pickle.load(archivo)
            return datos
    except FileNotFoundError:
        print(f"Error: Archivo {nombre_archivo} no encontrado")
    except IOError:
        print(f"Error: No se pudo leer el archivo {nombre_archivo}")

async def main() -> None:
    global opcion_dominio
    
    # Mostrar opciones de dominio al usuario 
    contador = 1
    for key in DOMINIOS_URL_CORTA.keys():
        print(f"{contador}. {key}")
        contador += 1
    opcion_dominio = int(input("\nIngrese una opción (1 - 5): ")) - 1
    print()

    await iniciar_proceso(CARACTERES, opcion_dominio)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except:
        # Guardar el estado en un archivo si ocurre un error durante la ejecución 
        guardar_estado(f"state_{opcion_dominio}.pkl", indices)
        print("\n\nEstado de ejecución guardado")