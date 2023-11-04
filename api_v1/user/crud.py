# from sqlalchemy import Result, select
from sqlalchemy import Result, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.dependencies import user_by_id
from api_v1.user.schemas import UserCreate, UserUpdatePartial
from core.models import User


# from sqlalchemy.orm import selectinload


class ExistStatus:
    EXISTS = "exists"
    NEW = "new"


async def create_user(session: AsyncSession, user_in: UserCreate) -> str:
    user = User(**user_in.model_dump())
    session.add(user)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "UniqueViolationError" in e.args[0]:
            return ExistStatus.EXISTS
    finally:
        await session.close()
    # await session.refresh(product)
    return ExistStatus.NEW


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_vk_id(session: AsyncSession, user_vk_id) -> User | None:
    stmt = select(User).where(User.vk_id == user_vk_id)
    result: Result = await session.execute(stmt)
    user = result.scalars().one()
    return user


async def update_user(
        user_update: UserUpdatePartial,
        user: User,
        session: AsyncSession,
        partial: bool = False,
) -> User | None:
    # обновляем атрибуты
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        if name != "vk_id":
            setattr(user, name, value)
    await session.commit()

    return user


async def archive_user(session: AsyncSession, user_id):
    stmt = update(User).where(User.id == user_id).values(archived=True)
    await session.execute(stmt)
    await session.commit()


async def restore_user(session: AsyncSession, user_id):
    stmt = update(User).where(User.id == user_id).values(archived=False)
    await session.execute(stmt)
    await session.commit()

# async def get_all_auto_drivers(session: AsyncSession, auto_id) -> list[Driver]:
#     stmt = select(Auto).options(selectinload(Auto.driver)).where(Auto.id == auto_id)
#     result: Result = await session.execute(stmt)
#
#     transport_unit_with_auto = result.scalars().one()
#     transport_units_with_id_drivers = transport_unit_with_auto.driver
#     id_drivers_list = [
#         transport_unit.driver_id for transport_unit in transport_units_with_id_drivers
#     ]
#
#     stmt = select(Driver).where(Driver.id.in_(id_drivers_list))
#     result: Result = await session.execute(stmt)
#     drivers = result.scalars().all()
#
#     return list(drivers)
#
#
# async def get_all_auto_routes(session: AsyncSession, auto_id) -> list[Route]:
#     stmt = select(Auto).options(selectinload(Auto.driver)).where(Auto.id == auto_id)
#     result: Result = await session.execute(stmt)
#
#     transport_unit_with_auto = result.scalars().one()
#     transport_units_with_id_drivers = transport_unit_with_auto.driver
#     id_transport_units = [
#         transport_unit.id for transport_unit in transport_units_with_id_drivers
#     ]
#
#     stmt = (
#         select(TrafficUnit)
#         .options(selectinload(TrafficUnit.route))
#         .where(TrafficUnit.transport_unit_id.in_(id_transport_units))
#     )
#     result: Result = await session.execute(stmt)
#
#     traffic_units = result.scalars().all()
#     routes = [traffic_unit.route for traffic_unit in traffic_units]
#     routes_unique = set(routes)
#
#     return list(routes_unique)
