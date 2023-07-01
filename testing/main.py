from decouple import config as getenv
import psycopg2

conn = psycopg2.connect(
    user=getenv("user"),
    password=getenv("password"),
    host=getenv("host"),
    port=getenv("port"),
    database=getenv("database"),
)

cursor = conn.cursor()

cursor.execute(
    """ CREATE TABLE if NOT EXISTS base_1 (
            id VARCHAR(10) PRIMARY KEY NOT NULL,
            redirect_url TEXT,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
)

conn.close()
