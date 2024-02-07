from uu import decode
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from starlette.middleware.cors import CORSMiddleware as CORSMiddleware

from api_v1 import router as router_v1
from core.config import settings

app = FastAPI()
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

origins = settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"Ping to the service root was successful!"}


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=True)

    # from datetime import datetime, timedelta
    # from typing import Any, Union

    # from fastapi import HTTPException
    # from jose import jwt, JWTError
    # from pydantic import ValidationError
    # from starlette import status

    # SECRET_KEY_JWT = "asdasdadada1267gdfdghtde3hds"
    # def create_access_token(user_id: Union[str, Any]) -> str:
    #     expires_delta = datetime.utcnow() + timedelta(minutes=30)

    #     payload = {"exp": expires_delta, "sub": str(user_id), "scope": "access_token"}
    #     encoded_jwt = jwt.encode(payload, SECRET_KEY_JWT, "HS256")
    #     return encoded_jwt
    
    # def decode_access_token(token: str) -> dict:
    #     return jwt.decode(token, SECRET_KEY_JWT, algorithms="HS256")
    
    # new_token = create_access_token(1)
    # print(new_token)

    # decoded = decode_access_token(new_token)
    # print(decoded)

