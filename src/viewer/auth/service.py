from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from pymongo.errors import DuplicateKeyError

from viewer.auth.schemas import SignUpSchema
from viewer.public.database import get_collection
from viewer.public.dependencies import get_user
from viewer.public.models import User
from viewer.public.utils import get_config


class Auth:
    """Authentication service class."""

    ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 7
    TOKEN_TYPE = "bearer"  # noqa: S105

    @classmethod
    def authenticate_user(cls, username: str, password: str) -> User | bool:
        """Authenticate a user by username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User | bool: The authenticated user object if authentication is successful,
                otherwise False.
        """
        user = get_user(username)
        if not user:
            return False
        if not cls.__verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def __verify_password(plain_password: str, hashed_password: bytes) -> bool:
        pwd_bytes = plain_password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hashed_password)

    @staticmethod
    def __hash_password(password: str) -> bytes:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """Create a JWT access token.

        Args:
            data (dict): The data to encode in the token.
            expires_delta (timedelta | None): The token expiration time.
                Defaults to 15 minutes.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            get_config("AUTH", "SECRET_KEY"),
            algorithm=get_config("AUTH", "ALGORITHM"),
        )

    @classmethod
    def add_user(cls, user: SignUpSchema) -> str:
        """Add a new user to the database.

        Args:
            user (SignUpSchema): The user data to add.

        Returns:
            str: An error message if the user could not be added, otherwise an empty
                string.
        """
        min_password_length = 6

        for attr in user:
            if not attr[1]:
                return "All fields are required."
        if " " in user.username or " " in user.password:
            return "Username cannot contain spaces."
        if len(user.password) < min_password_length:
            return f"Password must be at least {min_password_length} characters long."
        new_user = User(
            username=user.username,
            hashed_password=cls.__hash_password(user.password),
            add_date=datetime.now(UTC),
            role="user",
        )
        try:
            coll = get_collection("users")
            coll.insert_one(new_user.model_dump())
        except DuplicateKeyError:
            return "Username already exists."
        return ""
