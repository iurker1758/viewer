from viewer.public.schemas import BaseSchema


class Token(BaseSchema):
    """Schema for access token response."""

    access_token: str
    token_type: str


class SignUpSchema(BaseSchema):
    """Schema for user sign-up."""

    username: str
    password: str


class SignInSchema(BaseSchema):
    """Schema for user sign-in."""

    username: str
    password: str
