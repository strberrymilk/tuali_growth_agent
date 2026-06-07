import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DB_COMPANY_ONE = os.getenv("MONGO_DB_COMPANY_ONE", "")
MONGO_DB_COMPANY_TWO = os.getenv("MONGO_DB_COMPANY_TWO", "")

mongo_client: MongoClient | None = None

def get_mongo_client() -> MongoClient:
    global mongo_client

    if not MONGO_URI:
        raise ValueError("Missing MONGO_URI in environment variables.")

    if mongo_client is None:
        mongo_client = MongoClient(MONGO_URI)

    return mongo_client

def get_company_one_db() -> Database:
    if not MONGO_DB_COMPANY_ONE:
        raise ValueError("Missing MONGO_DB_COMPANY_ONE in environment variables.")

    return get_mongo_client()[MONGO_DB_COMPANY_ONE]

def get_company_two_db() -> Database:
    if not MONGO_DB_COMPANY_TWO:
        raise ValueError("Missing MONGO_DB_COMPANY_TWO in environment variables.")

    return get_mongo_client()[MONGO_DB_COMPANY_TWO]

def get_company_one_collection(collection_name: str):
    return get_company_one_db()[collection_name]

def get_company_two_collection(collection_name: str):
    return get_company_two_db()[collection_name]
