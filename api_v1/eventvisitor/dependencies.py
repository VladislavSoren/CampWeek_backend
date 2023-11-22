from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, EventVisitor

from . import crud


async def eventvisitor_by_id(
        obj_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> EventVisitor:
    obj = await crud.get_eventvisitor(session=session, eventvisitor_id=obj_id)
    if obj is not None:
        return obj

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"EventVisitor {obj_id} not found!",
    )
