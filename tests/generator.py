import string

# Crea una lista con todas las letras mayúsculas, minúsculas y dígitos
char_pool = string.ascii_letters + string.digits

# Función para generar una lista de todos los posibles IDs de longitud 5
def generate_all_ids():
    ids = []
    for c1 in char_pool:
        for c2 in char_pool:
            for c3 in char_pool:
                for c4 in char_pool:
                    for c5 in char_pool:
                        id = c1 + c2 + c3 + c4 + c5
                        ids.append(id)
    return ids

# Crea un DataFrame con una columna de IDs que contiene todos los posibles IDs
ids = generate_all_ids()

print(len(ids))

# IMPORTANTE: No ejecutar, a no ser que tenga una computadora cuántica
