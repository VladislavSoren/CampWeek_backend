from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException
from jose import jwt, JWTError
from pydantic import ValidationError
from starlette import status

from core import config

ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = config.settings.ALGORITHM
SECRET_KEY_JWT = config.SECRET_KEY_JWT
REFRESH_SECRET_KEY_JWT = config.REFRESH_SECRET_KEY_JWT


def create_access_token(user_id: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expires_delta, "sub": str(user_id), "scope": "access_token"}
    encoded_jwt = jwt.encode(payload, SECRET_KEY_JWT, ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_refresh_token(user_id: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expires_delta, "sub": str(user_id), "scope": "refresh_token"}
    encoded_jwt = jwt.encode(payload, REFRESH_SECRET_KEY_JWT, ALGORITHM)
    return encoded_jwt


def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, REFRESH_SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
