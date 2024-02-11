from sqlalchemy import Result, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.role.schemas import RoleCreate, RoleUpdatePartial
from core.models import Role


class ExistStatus:
    EXISTS = "exists"
    NEW = "new"


async def create_role(session: AsyncSession, role_in: RoleCreate) -> Role | str:
    role = Role(**role_in.model_dump())
    session.add(role)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "UniqueViolationError" in e.args[0]:
            return ExistStatus.EXISTS
    finally:
        await session.close()
    # await session.refresh(product)
    return role


async def get_all_roles(session: AsyncSession) -> list[Role]:
    stmt = select(Role).order_by(Role.id)
    result: Result = await session.execute(stmt)
    roles = result.scalars().all()
    return list(roles)


async def get_roles(session: AsyncSession) -> list[Role]:
    stmt = select(Role).order_by(Role.id).where(Role.archived.is_(False))
    result: Result = await session.execute(stmt)
    roles = result.scalars().all()
    return list(roles)


async def get_role(session: AsyncSession, role_id) -> Role | None:
    return await session.get(Role, role_id)


async def get_role_by_name(session: AsyncSession, name: str) -> Role | None:
    stmt = select(Role).where(Role.name == name)
    result: Result = await session.execute(stmt)
    role = result.scalars().first()
    return role


async def update_role(
    role_update: RoleUpdatePartial,
    role: Role,
    session: AsyncSession,
    partial: bool = False,
) -> Role | None:
    # обновляем атрибуты
    for name, value in role_update.model_dump(exclude_unset=partial).items():
        setattr(role, name, value)
    await session.commit()

    return role


async def archive_role(session: AsyncSession, role_id):
    stmt = update(Role).where(Role.id == role_id).values(archived=True)
    await session.execute(stmt)
    await session.commit()


async def restore_role(session: AsyncSession, role_id):
    stmt = update(Role).where(Role.id == role_id).values(archived=False)
    await session.execute(stmt)
    await session.commit()
