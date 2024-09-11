import psycopg2
from dotenv import load_dotenv
import os
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

DB_CONFIGS = [
        {
            'dbname': os.environ.get('DB_NAME'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'port': os.environ.get('DB_PORT'),
            
        },
        {
            'name': os.environ.get('DB_NAME_BACKUP'),
            'user': os.environ.get('DB_USER_BACKUP'),
            'password': os.environ.get('DB_PASSWORD_BACKUP'),
            'host': os.environ.get('DB_HOST_BACKUP'),
            'port': os.environ.get('DB_PORT_BACKUP'),
        }
    ]

def check_connection(db_configs):

    try:
        conn = psycopg2.connect(**db_configs)
        # Print to which database we are connected
        print(f"Conectado a la base de datos {db_configs['dbname']}")
        conn.close()
        return True
    except Exception as e:
        print(f"Fallo en la conexión a la base de datos. Error: {e}")
        return False
