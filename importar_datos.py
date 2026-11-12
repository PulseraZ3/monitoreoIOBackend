
import os
import json
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

BASE_DIR = Path(__file__).resolve().parent

CARPETA_REGISTROS = BASE_DIR / "registros"
ARCHIVO_CONTROL = BASE_DIR / "archivos_procesados.json"

load_dotenv(BASE_DIR / "atlas-credentials.env")

URI = os.getenv("MONGODB_URI")

cliente = MongoClient(URI)

db = cliente["monitoreo_iot"]
coleccion = db["mediciones_dht22"]

def cargar_archivos_procesados():

    if not ARCHIVO_CONTROL.exists():
        return []

    with open(ARCHIVO_CONTROL, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

    
def guardar_archivos_procesados(archivos):

    temporal = ARCHIVO_CONTROL.with_suffix(".tmp")

    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(archivos, archivo, indent=4)

    temporal.replace(ARCHIVO_CONTROL)


def importar_csv(ruta):

    df = pd.read_csv(
        ruta,
        sep=";",
        encoding="utf-8-sig"
    )

    documentos = df.to_dict(orient="records")

    for numero_fila, documento in enumerate(documentos, start=1):

        for columna, valor in documento.items():

            if pd.isna(valor):
                documento[columna] = None
        if documento["fecha_hora_recepcion_pc"] is not None:

            documento["fecha_hora_recepcion_pc"] = (
                pd.to_datetime(
                    documento["fecha_hora_recepcion_pc"],
                    utc=True
                ).to_pydatetime()
            )
        documento["archivo_origen"] = ruta.name
        documento["fila_origen"] = numero_fila

        # Insertar sin duplicar
        coleccion.update_one(
            {
                "archivo_origen": ruta.name,
                "fila_origen": numero_fila
            },
            {
                "$setOnInsert": documento
            },
            upsert=True
        )

    return len(documentos)

def main():

    archivos_procesados = cargar_archivos_procesados()

    archivos_csv = sorted(CARPETA_REGISTROS.glob("*.csv"))

    if not archivos_csv:
        print("No se encontraron archivos CSV.")
        return

    pendientes = [
        archivo for archivo in archivos_csv
        if archivo.name not in archivos_procesados
    ]

    if not pendientes:
        print("Todos los archivos ya fueron procesados.")
        return

    print(f"Archivos encontrados: {len(archivos_csv)}")
    print(f"Archivos pendientes: {len(pendientes)}")

    for archivo in pendientes:

        print(f"\nProcesando: {archivo.name}")

        cantidad = importar_csv(archivo)

        archivos_procesados.append(archivo.name)
        guardar_archivos_procesados(archivos_procesados)

        print(f"Registros procesados: {cantidad}")

    print("\nImportacion finalizada.")


if __name__ == "__main__":

    try:
        main()

    except Exception as error:
        print("Error durante la importacion:", error)

    finally:
        cliente.close()