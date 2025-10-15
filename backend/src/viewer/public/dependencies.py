import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from viewer.public.database import get_collection
from viewer.public.exceptions import CredentialsError
from viewer.public.models import User
from viewer.public.utils import get_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token extracted from the request.

    Returns:
        User: The user associated with the provided token.
    """
    try:
        payload = jwt.decode(
            token,
            get_config("AUTH", "SECRET_KEY"),
            algorithms=[get_config("AUTH", "ALGORITHM")],
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsError
    except jwt.InvalidTokenError:
        raise CredentialsError from None
    user = get_user(username)
    if user is None:
        raise CredentialsError
    return user


def get_user(username: str) -> User | None:
    """Retrieve a user from the database by username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        User | None: The user object if found, otherwise None.
    """
    coll = get_collection("users")
    user = coll.find_one({"username": username})
    if user is None:
        return user
    return User.model_validate(user)
