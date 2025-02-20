from __future__ import annotations
from typing import Literal
from pydantic import BaseModel

class Token(BaseModel):
    access_token : str
    token_type : Literal["bearer"] = "bearer"

    @classmethod
    def new(cls, access_token : str) -> "Token":
        return cls(access_token)
