from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt

from core import config

ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = config.settings.ALGORITHM
SECRET_KEY_JWT = config.SECRET_KEY_JWT
REFRESH_SECRET_KEY_JWT = config.REFRESH_SECRET_KEY_JWT


def create_access_token(user_id: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_JWT, ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY_JWT, ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    create_access_token("123")
