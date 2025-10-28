from pymongo import MongoClient
from pymongo.collection import Collection

from viewer.public.types import Database
from viewer.public.utils import get_config


def get_collection(coll: Database) -> Collection:
    """Get a MongoDB collection by name.

    Args:
        coll (Database): The name of the collection.

    Returns:
        Collection: The MongoDB collection object.
    """
    conn = MongoClient(get_config("DATABASE", "URI"))
    if coll in ("anilist", "royalroad", "last_updated"):
        db = conn.get_database("scraper")
    else:
        db = conn.get_database("viewer")
    return db[coll]
