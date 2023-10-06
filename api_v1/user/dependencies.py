from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Auto, db_helper

from . import crud


async def auto_by_id(
    auto_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Auto:
    auto = await crud.get_auto(session=session, auto_id=auto_id)
    if auto is not None:
        return auto

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Auto {auto_id} not found!",
    )
