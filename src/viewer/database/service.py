from scraper.anilist.fetcher import AniListFetcher
from scraper.royalroad.fetcher import RoyalRoadFetcher

from viewer.public.database import get_collection


class DatabaseService:
    """Service for interacting with different database collections."""

    def __init__(self, db: str) -> None:
        """Initialize the DatabaseService with the specified database collection.

        Args:
            db (str): The name of the database collection ("anilist" or "royalroad").
        """
        if db not in ("anilist", "royalroad"):
            raise ValueError("Invalid database name")
        self.db = db

    def get_all_documents(self) -> list[dict]:
        """Retrieve all documents from the specified database collection.

        Returns:
            list[dict]: A list of documents.
        """
        coll = get_collection(self.db)
        return coll.find()

    def update_database(self, page: str) -> None:
        """Update the specified database collection by fetching new data."""
        if self.db == "anilist":
            AniListFetcher(page=page).fetch()
        elif self.db == "royalroad":
            RoyalRoadFetcher(page=page).fetch()
