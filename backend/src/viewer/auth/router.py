from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from viewer.auth.exceptions import UnauthorizedError, create_login_error
from viewer.auth.schemas import SignInSchema, SignUpSchema, Token
from viewer.auth.service import Auth
from viewer.public.dependencies import get_current_user
from viewer.public.models import User
from viewer.public.schemas import UserSchema

router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(username: str) -> Token:
    """Create a JWT access token for the given username.

    Args:
        username (str): The username for which to create the token.

    Returns:
        Token: The JWT token for the authenticated user.
    """
    access_token_expires = timedelta(minutes=Auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Auth.create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type=Auth.TOKEN_TYPE,
    )


@router.post("/token")
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict:
    """Generate and return a JWT token for the authenticated user.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and
            password.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    user = Auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UnauthorizedError
    return create_access_token(user.username).model_dump()


@router.post("/sign-in")
async def sign_in(sign_in_data: SignInSchema) -> Token:
    """Sign in a user and return a JWT token.

    Args:
        sign_in_data (SignInSchema): The sign-in data containing username and password.

    Returns:
        Token: The JWT token for the authenticated user.
    """
    user = Auth.authenticate_user(sign_in_data.username, sign_in_data.password)
    if not user:
        raise UnauthorizedError
    return create_access_token(user.username)


@router.post("/sign-up")
async def sign_up(sign_up_data: SignUpSchema) -> Token:
    """Sign up a new user and return a JWT token.

    Args:
        sign_up_data (SignUpSchema): The sign-up data containing user details.

    Returns:
        Token: The JWT token for the newly created user.
    """
    error = Auth.add_user(sign_up_data)
    if error:
        raise create_login_error(error)
    return create_access_token(sign_up_data.username)


@router.get("/me")
def get_user(user: Annotated[User, Depends(get_current_user)]) -> UserSchema:
    """Get the current authenticated user's information."""
    return user.to_user_schema()
