from typing import Annotated

from fastapi import APIRouter, Depends

from viewer.database.schemas import DatabaseSchema, DatabaseUpdateSchema
from viewer.database.service import DatabaseService
from viewer.public.dependencies import get_current_user
from viewer.public.models import User

router = APIRouter(prefix="/database", tags=["database"])


@router.post("/")
def get_documents(
    params: DatabaseSchema,
    user: Annotated[User, Depends(get_current_user)],  # noqa: ARG001
) -> list[dict]:
    """Retrieve all documents from a database collection.

    Args:
        params (DatabaseSchema): The database schema containing the collection name.
        user (User): The current authenticated user.

    Returns:
        list[dict]: A list of documents from the collection.
    """
    return DatabaseService(params.db).get_all_documents()


@router.post("/update")
def update_database(
    params: DatabaseUpdateSchema,
    user: Annotated[User, Depends(get_current_user)],  # noqa: ARG001
) -> None:
    """Update a database collection by fetching new data.

    Args:
        params (DatabaseUpdateSchema): The database update schema containing the
            collection name and page.
        user (User): The current authenticated user.
    """
    DatabaseService(params.db).update_database(page=params.page)
