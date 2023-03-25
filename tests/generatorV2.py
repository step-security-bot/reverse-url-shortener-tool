## Author: ChatGPT

import itertools
import string
import csv

# Definimos la longitud de cada permutación y la cantidad de permutaciones por archivo
PERM_LENGTH = 5
PERMS_PER_FILE = 100000

# Definimos la lista de caracteres alfanuméricos a utilizar
ALPHANUM_CHARS = string.ascii_letters + string.digits

# Definimos el nombre del archivo de progreso
PROGRESS_FILENAME = 'progress.txt'

# Función para generar las permutaciones
def generate_permutations(start=0):
    # Calculamos el rango de permutaciones a generar
    end = start + PERMS_PER_FILE
    # Creamos un archivo para almacenar el progreso de este conjunto de permutaciones
    progress_file = open(f'progress_{start}.txt', 'w')
    
    # Generamos las permutaciones
    for i, perm in enumerate(itertools.product(ALPHANUM_CHARS, repeat=PERM_LENGTH), start=start):
        # Si llegamos al final del rango, cerramos el archivo y retornamos
        if i == end:
            progress_file.write(''.join(perm))
            progress_file.close()
            return
        
        # Escribimos la permutación en el archivo de progreso
        progress_file.write(''.join(perm))
        
        # Hacemos algo con la permutación generada, por ejemplo imprimirla
        print(perm)
        
    # Si llegamos al final de todas las permutaciones, cerramos el archivo
    progress_file.close()

# Función para continuar la generación de permutaciones desde el último progreso guardado
def resume_permutations():
    # Leemos el archivo de progreso para obtener la última permutación generada
    with open(PROGRESS_FILENAME, 'r') as progress_file:
        last_perm = progress_file.read()
    
    # Generamos las permutaciones a partir de la última permutación generada
    start = int(last_perm) + 1
    generate_permutations(start)

# Verificamos si hay un archivo de progreso y lo continuamos si es el caso, de lo contrario empezamos desde cero
try:
    resume_permutations()
except FileNotFoundError:
    generate_permutations()
