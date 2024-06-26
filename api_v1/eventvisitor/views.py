from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event.schemas import Event
from api_v1.event.views import EventActType
from api_v1.eventvisitor import crud
from api_v1.eventvisitor.dependencies import eventvisitor_by_id
from api_v1.eventvisitor.schemas import EventVisitor, EventVisitorCreate
from core.models import db_helper

# router
router = APIRouter(
    tags=["EventVisitor"],
)


@router.post("/", response_model=EventVisitor, status_code=status.HTTP_201_CREATED)
async def create_eventvisitor(
    eventvisitor_in: EventVisitorCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_eventvisitor(session=session, eventvisitor_in=eventvisitor_in)


@router.get("/", response_model=list[EventVisitor])
async def get_eventvisitors(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_eventvisitors(session=session)


@router.get("/{event_id}/", response_model=EventVisitor)
async def get_eventvisitor(
    eventvisitor: EventVisitor = Depends(eventvisitor_by_id),
    # token: str = Depends(oauth2_scheme)
):
    # token
    return eventvisitor


@router.get("/events_of/{visitor_id}/", response_model=list[Event])
async def get_events_of_visitor(
    visitor_id: int,
    actual_type: EventActType | None = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    events = await crud.get_events_by_visitor_id(session, visitor_id, actual_type)

    return events


@router.delete("/{event_id}/{user_id}/", response_model=dict)
async def delete(
    event_id: Annotated[int, Path],
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_obj(
        session=session,
        event_id=event_id,
        user_id=user_id,
    )
    return {"msg": f"User {user_id} was deleted from event {event_id}."}


# @router.get("/roles_of_user/{user_id}", response_model=list[Role])
# async def get_roles_of_user(
#         user_id: int,
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.get_roles_of_user(session=session, user_id=user_id)
#
#
# @router.get("/users_of_role/{role_id}", response_model=list[User])
# async def get_users_of_role(
#         role_id: int,
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.get_users_of_role(session=session, role_id=role_id)
