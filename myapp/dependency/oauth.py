from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from jose import jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi import HTTPException, status


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    try:

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    except HTTPException:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "failed to generate token"},
                headers={"X-Error": "internal error"}
        )


