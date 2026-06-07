import sys
from pathlib import Path


if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.database.mongo import get_aly_db, get_yomp_db


def test_mongo_connection() -> None:
    results: list[tuple[str, bool]] = []

    for label, getter in (("ALY", get_aly_db), ("YOMP", get_yomp_db)):
        print(f"\n--- Testing {label} ---")

        try:
            db = getter()
            collections = db.list_collection_names()
            print(f"Database: {db.name}")
            print(f"Collections: {collections}")

            if collections:
                sample = db[collections[0]].find_one({}, {"_id": 0})
                print(f"Sample document from {collections[0]}: {sample}")
            else:
                print("No collections found.")

            results.append((label, True))
        except Exception as error:
            print(f"{label} connection failed: {error}")
            results.append((label, False))

    assert any(success for _, success in results), "Neither MongoDB connection succeeded."


if __name__ == "__main__":
    test_mongo_connection()
