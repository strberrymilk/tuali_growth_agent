import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()

MONGODB_URI_ALY = os.getenv("MONGODB_URI_ALY", "")
MONGODB_URI_YOMP = os.getenv("MONGODB_URI_YOMP", "")
MONGODB_ALY = os.getenv("MONGODB_ALY", "")
MONGODB_YOMP = os.getenv("MONGODB_YOMP", "")

aly_mongo_client: MongoClient | None = None
yomp_mongo_client: MongoClient | None = None


def get_aly_mongo_client() -> MongoClient:
    global aly_mongo_client

    if not MONGODB_URI_ALY:
        raise ValueError("Missing MONGODB_URI_ALY in environment variables.")

    if aly_mongo_client is None:
        aly_mongo_client = MongoClient(MONGODB_URI_ALY)

    return aly_mongo_client


def get_yomp_mongo_client() -> MongoClient:
    global yomp_mongo_client

    if not MONGODB_URI_YOMP:
        raise ValueError("Missing MONGODB_URI_YOMP in environment variables.")

    if yomp_mongo_client is None:
        yomp_mongo_client = MongoClient(MONGODB_URI_YOMP)

    return yomp_mongo_client


def get_aly_db() -> Database:
    if not MONGODB_ALY:
        raise ValueError("Missing MONGODB_ALY in environment variables.")

    return get_aly_mongo_client()[MONGODB_ALY]


def get_yomp_db() -> Database:
    if not MONGODB_YOMP:
        raise ValueError("Missing MONGODB_YOMP in environment variables.")

    return get_yomp_mongo_client()[MONGODB_YOMP]


def get_aly_collection(collection_name: str):
    return get_aly_db()[collection_name]


def get_yomp_collection(collection_name: str):
    return get_yomp_db()[collection_name]
