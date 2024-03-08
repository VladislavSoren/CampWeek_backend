from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event import crud
from api_v1.event.dependencies import event_by_id
from api_v1.event.schemas import Event, EventCreate, EventUpdatePartial
from api_v1.event.utils import EventActType
from api_v1.userrole.dependencies import has_role
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
    actual_type: EventActType | None = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    # if isinstance(actual_type, str):
    #     actual_type = actual_type.lower().strip()

    if actual_type == "actual":
        return await crud.get_actual_events(session=session)
    elif actual_type == "passed":
        return await crud.get_passed_events(session=session)
    else:
        return await crud.get_events(session=session)


@router.get("/{event_id}/", response_model=Event)
async def get_event(
    event: Event = Depends(event_by_id),
):
    return event


@router.patch("/{event_id}/", response_model=Event)
async def update_event_partial(
    event_update: EventUpdatePartial,
    event: Event = Depends(event_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_event(
        event_update=event_update,
        event=event,
        session=session,
        partial=True,
    )


# here
@router.patch("/{event_id}/approve/", response_model=Event)
@has_role(["superadmin", "admin"])
async def approve_event(
    request: Request,
    event_update: EventUpdatePartial,
    event: Event = Depends(event_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    event.approved = True

    return await crud.update_event(
        event_update=event_update,
        event=event,
        session=session,
        partial=True,
    )


@router.patch("/{creator_id}/get-events/", response_model=list[Event])
async def get_events_of_creator(
    creator_id: int,
    actual_type: EventActType | None = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    events = await crud.get_events_by_creator_id(session, creator_id, actual_type)

    return events


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
