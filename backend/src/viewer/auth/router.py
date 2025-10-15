from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from viewer.auth.exceptions import UnauthorizedError
from viewer.auth.schemas import Token
from viewer.auth.service import Auth

router = APIRouter(prefix="/auth", tags=["auth"])


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
    access_token_expires = timedelta(minutes=Auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type=Auth.TOKEN_TYPE,
    ).model_dump()
