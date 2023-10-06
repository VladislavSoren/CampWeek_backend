from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Driver, db_helper

from . import crud


async def driver_by_id(
    driver_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Driver:
    driver = await crud.get_driver(session=session, driver_id=driver_id)
    if driver is not None:
        return driver

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Driver {driver_id} not found!",
    )
