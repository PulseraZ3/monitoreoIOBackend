
import os

from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING

load_dotenv("atlas-credentials.env")

uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("No se encontro MONGODB_URI")


cliente = MongoClient(uri)

db = cliente["monitoreo_iot"]

coleccion = db["mediciones_dht22"]
try:
    cantidad = coleccion.count_documents({})
    print("Total :", cantidad)
    resultados = coleccion.find(
        {},
        {
            "_id": 0,
            "temperatura_aire_c": 1,
            "humedad_relativa_aire_pct": 1,
            "fecha_hora_recepcion_pc": 1,
            "estado": 1
        }
    ).sort(
        "fecha_hora_recepcion_pc",
        DESCENDING
    ).limit(10)
    print("\nMediciones\n")

    for medicion in resultados:

        print("---------------------------")

        print(
            "Fecha:",
            medicion["fecha_hora_recepcion_pc"]
        )

        print(
            "Temperatura:",
            medicion.get("temperatura_aire_c"),
            "°C"
        )

        print(
            "Humedad:",
            medicion.get("humedad_relativa_aire_pct"),
            "%"
        )

        print(
            "Estado:",
            medicion["estado"]
        )

except Exception as error:

    print("Error:", error)

finally:

    cliente.close()
