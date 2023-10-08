# from sqlalchemy import Result, select
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.schemas import UserCreate
from core.models import User

# from sqlalchemy.orm import selectinload


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(product)
    return user


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id) -> User | None:
    return await session.get(User, user_id)


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
