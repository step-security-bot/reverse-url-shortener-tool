import string

# Todos los elementos que se van a permutar
CHARACTERS = string.ascii_letters + string.digits

def generate_permutations(elements, length):
    if length == 0:
        return [[]]

    permutations = []
    for i in range(len(elements)):
        current_element = elements[i]
        # Todos los elementos menos el actual (current)
        remaining_elements = elements[:i] + elements[i+1:]

        for sub_permutation in generate_permutations(remaining_elements, length - 1):
            new_permutation = [current_element] + sub_permutation
            permutations.append(new_permutation)

    return permutations


# Generar todas las permutaciones de longitud 2
permutations = generate_permutations(CHARACTERS, 3)

# Imprimir las permutaciones generadas
for permutation in permutations:
    print(permutation)
