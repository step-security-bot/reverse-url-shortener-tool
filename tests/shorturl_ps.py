from decouple import config as dec
import string
import random
import psycopg2

# Crea una lista con todas las letras mayúsculas, minúsculas y dígitos
char_pool = string.ascii_letters + string.digits

# Función para generar un ID alfanumérico aleatorio de longitud 5
def generate_random_id():
    return ''.join(random.choice(char_pool) for _ in range(5))

# Conecta con la base de datos PostgreSQL
conn = psycopg2.connect(
    host=dec("host"),
    database=dec("database"),
    user=dec("user"),
    password=dec("password")
)

# Crea una conexión
cur = conn.cursor()

# Genera 1000 IDs aleatorios y agrégales a la tabla
for i in range(1000):
    id = generate_random_id()
    cur.execute(f"INSERT INTO shorturl_base (id) VALUES ('{id}')")
conn.commit()

# Cierra la conexión con la base de datos
cur.close()
conn.close()
