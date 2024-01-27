from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper

from . import crud


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user: User = await crud.get_user(session=session, user_id=user_id)
    if user is not None:
        if user.archived is False:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} was archived!",
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


# from typing import Union, Any
# from datetime import datetime
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from .utils import (
#     ALGORITHM,
#     JWT_SECRET_KEY
# )
#
# from jose import jwt
# from pydantic import ValidationError
# from app.schemas import TokenPayload, SystemUser
# from replit import db
#
# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="/login",
#     scheme_name="JWT"
# )
#
#
# async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
#     try:
#         payload = jwt.decode(
#             token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#
#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Token expired",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except(jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
#
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Could not find user",
#         )
#
#     return SystemUser(**user)
