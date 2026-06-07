from __future__ import annotations

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


load_dotenv()


def _get_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


TUALI_URI = _get_env("MONGODB_URI_TUALI", "MONGODB_URI_ALY")
TUALI_DB_NAME = _get_env("MONGODB_TUALI", "MONGODB_ALY")
YOMP_URI = _get_env("MONGODB_URI_YOMP")
YOMP_DB_NAME = _get_env("MONGODB_YOMP")

_tuali_client: MongoClient | None = None
_yomp_client: MongoClient | None = None


def get_tuali_mongo_client() -> MongoClient:
    global _tuali_client

    if not TUALI_URI:
        raise ValueError(
            "Missing Tuali Mongo URI. Set MONGODB_URI_TUALI or MONGODB_URI_ALY in environment variables."
        )

    if _tuali_client is None:
        _tuali_client = MongoClient(TUALI_URI)

    return _tuali_client


def get_yomp_mongo_client() -> MongoClient:
    global _yomp_client

    if not YOMP_URI:
        raise ValueError("Missing Yomp Mongo URI. Set MONGODB_URI_YOMP in environment variables.")

    if _yomp_client is None:
        _yomp_client = MongoClient(YOMP_URI)

    return _yomp_client


def get_tuali_db() -> Database:
    if not TUALI_DB_NAME:
        raise ValueError(
            "Missing Tuali database name. Set MONGODB_TUALI or MONGODB_ALY in environment variables."
        )

    return get_tuali_mongo_client()[TUALI_DB_NAME]


def get_yomp_db() -> Database:
    if not YOMP_DB_NAME:
        raise ValueError("Missing Yomp database name. Set MONGODB_YOMP in environment variables.")

    return get_yomp_mongo_client()[YOMP_DB_NAME]


def get_tuali_collection(collection_name: str) -> Collection:
    return get_tuali_db()[collection_name]


def get_yomp_collection(collection_name: str) -> Collection:
    return get_yomp_db()[collection_name]


def get_company_one_db() -> Database:
    return get_tuali_db()


def get_company_two_db() -> Database:
    return get_yomp_db()


def get_company_one_collection(collection_name: str) -> Collection:
    return get_tuali_collection(collection_name)


def get_company_two_collection(collection_name: str) -> Collection:
    return get_yomp_collection(collection_name)
