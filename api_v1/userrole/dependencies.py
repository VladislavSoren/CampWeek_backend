from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, UserRole

from functools import wraps
from typing import Callable, Union

from api_v1.auth.auth_bearer import JWTBearerAccess
from api_v1.userrole import crud


async def userrole_by_id(
    obj_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserRole:
    obj = await crud.get_userrole(session=session, userrole_id=obj_id)
    if obj is not None:
        return obj

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"UserRole {obj_id} not found!",
    )


def has_role(required_roles: Union[str, list[str]]) -> Callable:
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            access_token: dict = Depends(JWTBearerAccess()),
            session: AsyncSession = Depends(db_helper.scoped_session_dependency),
            *args,
            **kwargs,
        ):
            user_id = access_token["sub"]
            user_roles = await crud.get_roles_of_user(session, user_id)
            user_role_names = {role.name for role in user_roles}

            if any(role in user_role_names for role in required_roles):
                return await func(*args, session=session, **kwargs)
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You do not have any of the required roles to perform this action",
                )

        return wrapper

    return decorator
