from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event import crud
from api_v1.event.dependencies import event_by_id
from api_v1.event.schemas import Event, EventCreate
from core.models import db_helper

router = APIRouter(
    tags=["Event"],
)


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_event(session, event_in)


@router.get("/", response_model=list[Event])
async def get_events(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_events(session=session)


@router.get("/{event_id}/", response_model=Event)
async def get_event(
    event: Event = Depends(event_by_id),
):
    return event
#
#
# @router.get("/{driver_id}/autos/", response_model=list[Auto])
# async def get_all_driver_autos(
#     driver_id: int,
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
#     _: Driver = Depends(driver_by_id),  # check if user is exist
# ):
#     return await crud.get_all_driver_autos(session, driver_id)
#
#
# @router.get("/{driver_id}/routes/", response_model=list[Route])
# async def get_all_driver_routes(
#     driver_id: int,
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
#     _: Driver = Depends(driver_by_id),  # check if user is exist
# ):
#     return await crud.get_all_driver_routes(session, driver_id)
