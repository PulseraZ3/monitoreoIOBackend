import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv("./atlas-credentials.env")
uri = os.getenv("MONGODB_URI")
if not uri:
    raise ValueError("No se encontro MONGODB_URI en el archivo .env")

cliente = MongoClient(
    uri,
    serverSelectionTimeoutMS=5000
)
try:
    cliente.admin.command("ping")
    print("conexion")
    db = cliente["monitoreoiot"]
    print("Base de datos :",db.name)
except Exception as error:
    print("Error conexion", error)
finally:
    cliente.close()