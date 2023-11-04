from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Role, db_helper

from . import crud


async def role_by_id(
    role_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Role:
    role = await crud.get_role(session=session, role_id=role_id)
    if role is not None:
        if role.archived is False:
            return role
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role {role_id} was archived!",
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Role {role_id} not found!",
    )
