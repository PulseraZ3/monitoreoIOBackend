import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

load_dotenv("./atlas-credentials.env")
uri = os.getenv("MONGODB_URI")
if not uri:
    raise ValueError("No se encontro MONGODB_URI en el archivo .env")

cliente = MongoClient(uri)

try:
    
    cliente.admin.command("ping")
    db = cliente["monitoreo_iot"]
    mediciones = db["mediciones_dht22"]
    mediciones.create_index(
        [
            ("archivo_origen", ASCENDING),
            ("fila_origen", ASCENDING)
        ],
        unique=True
    )
    print("Base de datos configurada")
    print("coleccion: ", mediciones.name)
    print("Indice unico creado")
except Exception as error:
    print("Error conexion", error)
finally:
    cliente.close()