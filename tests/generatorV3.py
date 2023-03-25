## Author: ChatGPT

import itertools
import csv
import os
import hashlib


# Constantes
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHUNK_SIZE = 1000000
PROGRESS_FILENAME = "progress.csv"

# Funciones
def generate_permutations():
    # Verificar si existe un archivo de progreso previo
    start_point = 0
    if os.path.exists(PROGRESS_FILENAME):
        with open(PROGRESS_FILENAME, newline='') as csvfile:
            reader = csv.reader(csvfile)
            last_row = list(reader)[-1]
            last_perm = last_row[0]
            start_point = int(last_row[1]) + 1
            print(f"Reanudando desde la permutación {last_perm}, en la posición {start_point}")

    # Generar permutaciones en bloques
    for i in range(start_point, len(ALPHABET)**4):
        perms = itertools.product(ALPHABET, repeat=4)
        perms = itertools.islice(perms, i, None, CHUNK_SIZE)

        with open(PROGRESS_FILENAME, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for perm in perms:
                # Guardar permutación y posición en el archivo de progreso
                writer.writerow([''.join(perm), i])

                # Calcular un hash de la permutación en base 32 y verificar si es múltiplo del tamaño de bloque
                if int(hashlib.sha1(''.join(perm).encode()).hexdigest(), 16) % CHUNK_SIZE == 0:
                    print(f"Progreso: {i} permutaciones, última permutación: {''.join(perm)}")

                    # Guardar la permutación en un archivo separado
                    with open(f"{i}.csv", mode='a', newline='') as permfile:
                        permwriter = csv.writer(permfile)
                        permwriter.writerow([''.join(perm)])

def resume_permutations():
    # Verificar si existe un archivo de progreso previo
    if os.path.exists(PROGRESS_FILENAME):
        with open(PROGRESS_FILENAME, newline='') as csvfile:
            reader = csv.reader(csvfile)
            last_row = list(reader)[-1]
            last_perm = last_row[0]
            start_point = int(last_row[1]) + 1
            print(f"Reanudando desde la permutación {last_perm}, en la posición {start_point}")
            return

    print("No se encontró archivo de progreso previo.")

# Programa principal
if __name__ == "__main__":
    # Verificar si ya existe un archivo de progreso
    resume_permutations()

    # Generar permutaciones
    generate_permutations()
