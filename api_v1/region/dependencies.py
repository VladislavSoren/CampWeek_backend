from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Region, db_helper

from . import crud


async def region_by_id(
    region_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Region:
    region = await crud.get_region(session=session, region_id=region_id)
    if region is not None:
        if region.archived is False:
            return region
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Region {region_id} was archived!",
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Region {region_id} not found!",
    )
