from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event.schemas import Event
from api_v1.eventspeaker import crud
from api_v1.eventspeaker.dependencies import eventspeaker_by_id
from api_v1.eventspeaker.schemas import EventSpeaker, EventSpeakerCreate
from api_v1.userrole.dependencies import has_role
from core.models import db_helper

# router
router = APIRouter(
    tags=["EventSpeaker"],
)


@router.post("/", response_model=EventSpeaker, status_code=status.HTTP_201_CREATED)
async def create_eventspeaker(
    eventspeaker_in: EventSpeakerCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_eventspeaker(session=session, eventspeaker_in=eventspeaker_in)


@router.get("/", response_model=list[EventSpeaker])
async def get_eventspeakers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_eventspeakers(session=session)


@router.get("/{eventspeaker_id}/", response_model=EventSpeaker)
async def get_eventspeaker(
    eventspeaker: EventSpeaker = Depends(eventspeaker_by_id),
    # token: str = Depends(oauth2_scheme)
):
    # token
    return eventspeaker


# here
@router.post("/{event_id}/add-speakers/", response_model=list[EventSpeaker])
@has_role(["superadmin", "admin"])
async def add_speakers_to_event(
    request: Request,
    speakers: list[EventSpeakerCreate],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    added_speakers = []
    for speaker in speakers:
        event_speaker = await crud.create_eventspeaker(
            session=session,
            eventspeaker_in=speaker,
        )
        added_speakers.append(event_speaker)

    return added_speakers


@router.get("/{speaker_id}/get-events/", response_model=list[Event])
async def get_events_of_speaker(
    speaker_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    events = await crud.get_events_by_speaker_id(session, speaker_id)

    return events


#
# @router.patch("/{obj_id}/", response_model=UserRole)
# async def update_userrole_partial(
#         userrole_update: UserRoleUpdatePartial,
#         userrole: UserRole = Depends(userrole_by_id),
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     return await crud.update_userrole(
#         userrole_update=userrole_update,
#         userrole=userrole,
#         session=session,
#         partial=True,
#     )
#
#
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
