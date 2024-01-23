from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, UserRole

from . import crud

from functools import wraps
from typing import Callable


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


def has_role(required_role: str) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            *args,
            requesting_user_id: int = Depends(userrole_by_id),
            session: AsyncSession = Depends(db_helper.scoped_session_dependency),
            **kwargs
        ):
            user_roles = await crud.get_roles_of_user(session, requesting_user_id)
            user_role_names = {role.name for role in user_roles}

            if required_role in user_role_names:
                return await func(*args, session=session, **kwargs)
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You do not have the required role ({required_role}) to perform this action",
                )

        return wrapper

    return decorator