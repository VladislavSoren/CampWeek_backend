from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event.schemas import Driver
from api_v1.route.schemas import Route
from api_v1.user import crud
from api_v1.user.dependencies import auto_by_id
from api_v1.user.schemas import Auto, AutoCreate
from core.models import db_helper

router = APIRouter(
    tags=["Auto"],
)


@router.post("/", response_model=Auto, status_code=status.HTTP_201_CREATED)
async def create_auto(
    auto_in: AutoCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_auto(session, auto_in)


@router.get("/", response_model=list[Auto])
async def get_autos(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_autos(session=session)


@router.get("/{auto_id}/", response_model=Auto)
async def get_auto(
    auto: Auto = Depends(auto_by_id),
):
    return auto


@router.get("/{auto_id}/drivers/", response_model=list[Driver])
async def get_all_auto_drivers(
    auto_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    _: Auto = Depends(auto_by_id),  # check if user is exist
):
    return await crud.get_all_auto_drivers(session, auto_id)


@router.get("/{auto_id}/routes/", response_model=list[Route])
async def get_all_auto_routes(
    auto_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    _: Auto = Depends(auto_by_id),  # check if user is exist
):
    return await crud.get_all_auto_routes(session, auto_id)
