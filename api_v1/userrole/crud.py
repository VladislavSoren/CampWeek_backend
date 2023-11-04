from fastapi import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.role.schemas import UserRoleCreate, UserRoleUpdatePartial
from core.models import UserRole


class ExistStatus:
    EXISTS = "exists"
    NEW = "new"


class db_exception(Exception):
    pass


async def create_userrole(session: AsyncSession, userrole_in: UserRoleCreate) -> UserRole | str:
    obj = UserRole(**userrole_in.model_dump())
    session.add(obj)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "UniqueViolationError" in e.args[0]:
            return ExistStatus.EXISTS
        if "is not present in table" in e.args[0]:
            # raise db_exception("Key is not present in table")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="DB_exception: Key is not present in table",
            )
    finally:
        await session.close()
    # await session.refresh(product)
    return obj


async def get_userroles(session: AsyncSession) -> list[UserRole]:
    stmt = select(UserRole).order_by(UserRole.id)
    result: Result = await session.execute(stmt)
    objs = result.scalars().all()
    return list(objs)


async def get_userrole(session: AsyncSession, userrole_id) -> UserRole | None:
    return await session.get(UserRole, userrole_id)


async def update_userrole(
        userrole_update: UserRoleUpdatePartial,
        userrole: UserRole,
        session: AsyncSession,
        partial: bool = False,
) -> UserRole | None:
    # обновляем атрибуты
    for name, value in userrole_update.model_dump(exclude_unset=partial).items():
        setattr(userrole, name, value)

    try:
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'''DB_exception: {e.args[0].split("DETAIL:")[-1].strip()}''',
        )
    return userrole

# get roles of user

# get users with this role
