
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