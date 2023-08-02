import mysql.connector
from mysql.connector import Error
from decouple import config as getenv


def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=getenv("DB_HOST", "127.0.0.1"),
            port=getenv("DB_PORT", "3306"),
            database=getenv("DB_DATABASE", "forge"),
            user=getenv("DB_USERNAME", "forge"),
            password=getenv("DB_PASSWORD", ""),
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci",
        )

        if connection.is_connected():
            print("Conexión exitosa a la base de datos MySQL.")
            return connection

    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")

    return None


# Ejemplo de uso
connection = connect_to_mysql()
if connection is not None:
    # Aquí puedes realizar tus consultas a la base de datos
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tu_tabla")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    connection.close()
