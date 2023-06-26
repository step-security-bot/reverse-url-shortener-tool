import string

CHARACTERS = string.ascii_letters + string.digits

def generate_permutations(characters: str, length: int) -> None:
    num_characters = len(characters)

    # Inicializar el arreglo de índices con la longitud deseada
    indices = [0] * length

    # Generar las permutaciones iterativamente
    while True:
        # Permutación actual usando el arreglo de índices y la lista de caracteres
        permutation = [characters[i] for i in indices]
        print(''.join(permutation))

        # Encontrar el siguiente índice a incrementar
        i = length - 1
        # Mientras los números a la derecha sean los máximos, moverse a la izquierda
        while i >= 0 and indices[i] == num_characters - 1:
            i -= 1

        # Si todos los índices han alcanzado el máximo, terminar el bucle
        if i < 0:
            break

        # Incrementar el índice encontrado y ajustar los siguientes índices de la derecha a 0
        indices[i] += 1
        for j in range(i + 1, length):
            indices[j] = 0

# Generar todas las permutaciones de longitud 4
generate_permutations(CHARACTERS, 4)
