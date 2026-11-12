import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv("./atlas-credentials.env")
uri = os.getenv("MONGODB_URI")
