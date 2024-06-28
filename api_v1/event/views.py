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
    # request: Request,
    actual_type: EventActType | None = None,
    offset: int = 0,
    limit: int = 5,
    approved: bool = None,
    region_ids: str | None = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    events = await crud.get_events(session, actual_type, offset, limit, approved, region_ids)
    return events


@router.get("/of_creator/{creator_id}", response_model=list[Event])
async def get_events_of_creator(
    creator_id: int,
    actual_type: EventActType | None = None,
    offset: int = 0,
    limit: int = 5,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    events = await crud.get_events_by_creator_id(session, creator_id, actual_type, offset, limit)

    return events


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
@has_role(["superadmin", "admin", "admin_test"])
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
