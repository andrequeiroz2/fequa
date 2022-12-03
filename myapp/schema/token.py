from pydantic import BaseModel
from typing import Union


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataSchema(BaseModel):
    username: Union[str, None] = None
