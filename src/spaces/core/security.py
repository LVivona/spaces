from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

import jwt

from passlib.context import CryptContext

from spaces.core.config import settings
from enum import Enum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


class GitAccessType(Enum):
    W = 0
    R = 1
    RW = 2

    @classmethod
    def from_int(cls, kind: int) -> "GitAccessType":
        if kind == 0:
            return GitAccessType.W
        elif kind == 1:
            return GitAccessType.R
        elif kind == 2:
            return GitAccessType.RW
        else:
            ValueError("Integer can not be greater then 2 or less then 0")


def create_jwt_access_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    """
    Creating an access token

    Args:
        subject (str | Any): extra information that could be serialized json or just an email.
        expires_delta (timedelta): expiry date to when the token is not valid

    Returns:
        str: _description_
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_read_write_token(repo_path: str, username: str, kind: GitAccessType) -> str:
    """
    Create access token to repository that will be use to validate if user can clone,
    and push to the remote repo.

    Args:
        repo_path (str): path to the repo to access


    """
    to_encode = {"repo_path": repo_path, "username": username, "access": kind}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    verify plaintext with cyphered-text

    Args:
        plain_password (str): un-hashed string
        hashed_password (str): hashed string

    Returns:
        bool: True if the hash-password is equal to the un-hashed password, else False
    """
    return pwd_context.verify(plain_password, hashed_password)


def verify_expired(token: Optional[str] = None) -> bool:
    """
    Verify if a JWT token has expired by checking its expiration timestamp.

    Args:
        token (str | None): The JWT token to verify

    Returns:
        Dict[str, Any]: The decoded payload if valid

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
        ValueError: If token doesn't contain expiration claim
    """
    try:
        if token is None:
            return True

        # Decode the token without verification first to check exp claim
        payload = jwt.decode(
            token,
            options={"verify_signature": False},  # First pass without verification
        )

        # Check if expiration claim exists
        if (exp_timestamp := payload.get("exp")) is None:
            raise ValueError("Token has no expiration claim")

        # Get current timestamp
        current_timestamp = datetime.noe().timestamp()

        # Check if token has expired
        if current_timestamp > exp_timestamp:
            return True

        # If we get here then it is not expired
        return False

    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")
    except Exception as e:
        raise ValueError(f"Token verification failed: {str(e)}")


def access_type(user: str, token: str) -> GitAccessType:
    """
    check the access of the user token to said repository

    Args:
        user: person who made request to the repo
        token: string token that was signed from the repo owner that allows other to
               read, write or both to the repo.

    Return:
        GitAccessType: enum that repersents the user status on the repo.

    Rasie:
        KeyError
        InvalidTokenError: If token is invalid
    """

    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": True},
        )
    except KeyError as k:
        raise k
    except jwt.InvalidTokenError as _:
        raise Exception("Token was invalid")


def get_password_hash(password: str) -> str:
    """return hash password"""
    return pwd_context.hash(password)
