from __future__ import annotations
import secrets
from typing import Annotated, Any

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from spaces.core.security import GitAccessType, access_type

_security = HTTPBasic()

def _validate_git_access(credentials: UserCredential) -> GitAccessType:
    """
    Dependency function that check the user crednetial of a Basic
    HTTP Credentials within the request header

    Return:
        GitAccessType: enum that repersents the user status on the repo.
    """
    # TODO: check what ever database if the user exsit in db for now.
    try:
        client_id = secrets.compare_digest(credentials.username, "admin")

        if not client_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        # NOTE: all access tokens should be stored in the database but they should
        #       also be hashed like password.
        # TODO: add qeury db check for token signed under user.
        # Pros: 
        #       - robust securiy
        # Cons:
        #       - slower run time
    
        # if useranem is in the db check the access
        client_secret = access_type(credentials.password)

    except Exception as e:
        raise e

    return client_secret

def _validate_user_access(credentials: UserCredential) -> Any: 
    ...

UserCredential = Annotated[HTTPBasicCredentials, Depends(_security)]
GitAuthentication = Annotated[GitAccessType, Depends(_validate_git_access)]

"""
Used for jwt based token authentication, allowing user to 
read, and write on there repo's.
"""
WebAuthentication = Annotated[Any, Depends(_validate_user_access)]


