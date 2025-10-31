from datetime import datetime

from pydantic import BaseModel

from viewer.public.schemas import UserSchema


class User(BaseModel):
    """Schema for user data."""

    username: str
    hashed_password: bytes
    add_date: datetime
    role: str

    def to_user_schema(self) -> UserSchema:
        """Convert the User model to a UserSchema.

        Returns:
            UserSchema: The user data.
        """
        return UserSchema(
            username=self.username,
            role=self.role,
        )
