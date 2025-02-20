from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic

from spaces.models import Token
from spaces.core import security
from spaces.deps import WebAuthentication

router = APIRouter()

def _is_user(username : str, password : str):...

@router.post(
    "/login",
    response_description="login authorization",
    response_model=Token,
)
async def login_access_token(
    form_data: WebAuthentication
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    and update the user's stored token.

    Args:
        db : Database session
        form_data: OAuth2 password request form

    Returns:
        Token: Access token for authentication

    Raises:
        HTTPException: If authentication fails
    """
    
    username = form_data.username
    password = form_data.password

    if not _is_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )


    try:
        # TODO: check database for user


        # TODO: change this to user ID.
        subject = dict(username)
        access_token = security.create_jwt_access_token(subject=subject)

        return Token.new(access_token)
    except Exception as e :
        raise e
    
