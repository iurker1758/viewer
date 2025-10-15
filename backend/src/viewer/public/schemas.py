from pydantic import BaseModel


class UserSchema(BaseModel):
    """Schema for user information."""

    username: str
    first_name: str
    last_name: str
    email: str
    role: str
