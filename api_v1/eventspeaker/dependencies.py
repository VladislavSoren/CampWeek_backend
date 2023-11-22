from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, EventSpeaker

from . import crud


async def eventspeaker_by_id(
        obj_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> EventSpeaker:
    obj = await crud.get_eventspeaker(session=session, eventspeaker_id=obj_id)
    if obj is not None:
        return obj

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"EventSpeaker {obj_id} not found!",
    )
