from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_access_token, decode_refresh_token


class JWTBearerAccess(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerAccess, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAccess, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            access_token = credentials.credentials
            decoded_access_token = decode_access_token(access_token)
            return decoded_access_token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def check_access_token(access_token_str):
    if 'Bearer' not in access_token_str:
        raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
    access_token = access_token_str.split('Bearer')[-1].strip()
    decoded_access_token = decode_access_token(access_token)
    return decoded_access_token


class JWTBearerRefresh(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerRefresh, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerRefresh, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            access_token = credentials.credentials
            decoded_access_token = decode_refresh_token(access_token)
            return decoded_access_token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
