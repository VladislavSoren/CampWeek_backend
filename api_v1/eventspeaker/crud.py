from fastapi import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from api_v1.eventspeaker.schemas import EventSpeakerCreate, EventSpeakerUpdatePartial
from core.models import EventSpeaker, User, Role


class ExistStatus:
    EXISTS = "exists"
    NEW = "new"


class db_exception(Exception):
    pass


async def create_eventspeaker(session: AsyncSession, eventspeaker_in: EventSpeakerCreate) -> EventSpeaker | str:
    obj = EventSpeaker(**eventspeaker_in.model_dump())
    session.add(obj)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "UniqueViolationError" in e.args[0]:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail=f'''DB_exception (UniqueViolationError): {e.args[0].split("DETAIL:")[-1].strip()}''',
            )
        if "ForeignKeyViolationError" in e.args[0]:
            # raise db_exception("Key is not present in table")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'''DB_exception (ForeignKeyViolationError): {e.args[0].split("DETAIL:")[-1].strip()}''',
            )
    finally:
        await session.close()
    # await session.refresh(product)
    return obj


async def get_eventspeakers(session: AsyncSession) -> list[EventSpeaker]:
    stmt = select(EventSpeaker).order_by(EventSpeaker.id)
    result: Result = await session.execute(stmt)
    objs = result.scalars().all()
    return list(objs)


async def get_eventspeaker(session: AsyncSession, eventspeaker_id) -> EventSpeaker | None:
    return await session.get(EventSpeaker, eventspeaker_id)


# async def update_userrole(
#         userrole_update: UserRoleUpdatePartial,
#         userrole: UserRole,
#         session: AsyncSession,
#         partial: bool = False,
# ) -> UserRole | None:
#     # обновляем атрибуты
#     for name, value in userrole_update.model_dump(exclude_unset=partial).items():
#         setattr(userrole, name, value)
# 
#     try:
#         await session.commit()
#     except IntegrityError as e:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'''DB_exception (ForeignKeyViolationError): {e.args[0].split("DETAIL:")[-1].strip()}''',
#         )
#     return userrole
# 
# 
# async def get_roles_of_user(session: AsyncSession, user_id: int) -> list[Role]:
#     stmt = select(UserRole).options(joinedload(UserRole.role)).where(UserRole.user_id == user_id)
#     result: Result = await session.execute(stmt)
#     objs = result.scalars().all()
# 
#     roles_list = [obj.role for obj in objs]
# 
#     return roles_list
# 
# 
# async def get_users_of_role(session: AsyncSession, role_id: int) -> list[User]:
#     stmt = select(UserRole).options(joinedload(UserRole.user)).where(UserRole.role_id == role_id)
#     result: Result = await session.execute(stmt)
#     objs = result.scalars().all()
# 
#     users_list = [obj.user for obj in objs]
# 
#     return users_list
