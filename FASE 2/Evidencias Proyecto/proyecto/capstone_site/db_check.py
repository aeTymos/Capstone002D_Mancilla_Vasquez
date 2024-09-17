import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import OperationalError
import time
import random

load_dotenv()

DB_1 = {
    'HOST': os.environ.get('DB_HOST'),
    'PORT': os.environ.get('DB_PORT'),
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
}

DB_2 = {
    'HOST': os.environ.get('DB_HOST_BACKUP'),
    'PORT': os.environ.get('DB_PORT_BACKUP'),
    'NAME': os.environ.get('DB_NAME_BACKUP'),
    'USER': os.environ.get('DB_USER_BACKUP'),
    'PASSWORD': os.environ.get('DB_PASSWORD_BACKUP'),
}

def check_connection(**kwargs):

    host = kwargs.get('HOST')
    port = kwargs.get('PORT')
    database = kwargs.get('NAME')
    user = kwargs.get('USER')
    password = kwargs.get('PASSWORD')
    retries = kwargs.get('retries', 1)
    delay = kwargs.get('delay', 1)

    intento = 0

    while intento < retries:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=database,
                user=user,
                password=password
            )
            # Print to which database we are connected
            print(f"Conectado a la base de datos {database}, en el host {host}:{port} como usuario {user}.")
            print(f"Estado de la conexión: {conn.status}")
            conn.close()
            return True
        except OperationalError as e:
            print(f"Intento {intento + 1} de conexión a {host}:{port} fallido: {e}")
            intento += 1
            time.sleep(delay * (2 ** intento) + random.uniform(0, 1))
    return False