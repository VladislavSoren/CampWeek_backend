from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Event, db_helper

from . import crud


async def event_by_id(
    event_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Event:
    event = await crud.get_event(session=session, event_id=event_id)
    if event is not None:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Event {event_id} not found!",
    )
