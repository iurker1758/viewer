from pydantic import BaseModel


class Token(BaseModel):
    """Schema for access token response."""

    access_token: str
    token_type: str


class SignUpSchema(BaseModel):
    """Schema for user sign-up."""

    username: str
    password: str
    first_name: str
    last_name: str
    email: str


class SignInSchema(BaseModel):
    """Schema for user sign-in."""

    username: str
    password: str
