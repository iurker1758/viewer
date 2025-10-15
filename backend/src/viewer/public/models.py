from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    """Schema for user data."""

    username: str
    hashed_password: bytes
    first_name: str
    last_name: str
    email: str
    add_date: datetime
    role: str
