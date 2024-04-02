from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.region import crud
from api_v1.region.dependencies import region_by_id
from api_v1.region.schemas import Region, RegionCreate
from core.models import db_helper

# router
router = APIRouter(
    tags=["Region"],
)


@router.post("/", response_model=Region, status_code=status.HTTP_201_CREATED)
async def create_region(
    region_in: RegionCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_region(session=session, region_in=region_in)


@router.get("/", response_model=list[Region])
async def get_regions(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_regions(session=session)


@router.get("/{region_id}/", response_model=Region)
async def get_region(
    region: Region = Depends(region_by_id),
):
    return region


@router.delete("/{region_id}/", response_model=dict)
async def delete(
    region_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_obj(
        session=session,
        region_id=region_id,
    )
    return {"msg": f"Region {region_id} was deleted."}
