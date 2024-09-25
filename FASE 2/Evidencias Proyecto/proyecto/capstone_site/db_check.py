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

DB_3 = {
    'HOST': os.environ.get('DB_HOST_BACKUP_2'),
    'PORT': os.environ.get('DB_PORT_BACKUP_2'),
    'NAME': os.environ.get('DB_NAME_BACKUP_2'),
    'USER': os.environ.get('DB_USER_BACKUP_2'),
    'PASSWORD': os.environ.get('DB_PASSWORD_BACKUP_2'),    
}

available_db = None

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
        tiempo_inicio = time.time()
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=database,
                user=user,
                password=password,
                connect_timeout=2
            )
            # Print to which database we are connected
            print(f"Conectado a la base de datos {database}, en el host {host}:{port} como usuario {user}. Tiempo de operación: {time.time() - tiempo_inicio:.2f} segundos")
            conn.close()
            return True
        except OperationalError as e:
            print(f"Intento {intento + 1} de conexión a {host}:{port} fallido: {e} después de {time.time() - tiempo_inicio:.2f} segundos")
            intento += 1
            time.sleep(delay * (2 ** intento) + random.uniform(0, 1))
    return False

def get_database():
    global available_db
    if available_db is not None:
        return available_db
    
    databases = [DB_1, DB_2, DB_3]

    for db_config in databases:
        if check_connection(**db_config):
            available_db = db_config
            return db_config
    raise Exception('No se pudo establecer conexión con ninguna base de datos.')