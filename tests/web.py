from decouple import config as dec
import psycopg2
import requests

domain = 'https://www.shorturl.at/'

# Conecta con la base de datos PostgreSQL
conn = psycopg2.connect(
    host=dec("host"),
    database=dec("database"),
    user=dec("user"),
    password=dec("password")
)
cur = conn.cursor()

cur.execute('SELECT * FROM shorturl_base;')

output = cur.fetchall()
counter = 1
for i in output:
    response = requests.get(domain + i[0])

    if response.history:
        print(counter, response.url)
    else:
        print("No se encontraron redirecciones.")
    counter += 1

cur.close()
conn.close()
