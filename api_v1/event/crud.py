from datetime import datetime

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.event.schemas import EventCreate, EventUpdatePartial
from core.models import Event


async def create_event(session: AsyncSession, event_in: EventCreate) -> Event:
    event = Event(**event_in.model_dump())
    session.add(event)
    await session.commit()
    # await session.refresh(product)
    return event


async def get_events(session: AsyncSession) -> list[Event]:
    stmt = select(Event).order_by(Event.id)
    result: Result = await session.execute(stmt)
    events = result.scalars().all()
    return list(events)


async def get_actual_events(session: AsyncSession) -> list[Event]:
    """
    Actual event:
    - date_time > current_time
    - is NOT deleted
    """

    current_time = datetime.now()

    stmt = select(Event).order_by(Event.id).filter(
        Event.date_time > current_time
    )
    result: Result = await session.execute(stmt)
    events = result.scalars().all()
    return list(events)


async def get_event(session: AsyncSession, event_id) -> Event | None:
    return await session.get(Event, event_id)


async def update_event(
        event_update: EventUpdatePartial,
        event: Event,
        session: AsyncSession,
        partial: bool = False,
) -> Event | None:
    # обновляем атрибуты
    for name, value in event_update.model_dump(exclude_unset=partial).items():
        setattr(event, name, value)
    await session.commit()

    return event

# async def get_all_driver_autos(session: AsyncSession, driver_id) -> list[Auto]:
#     stmt = (
#         select(Driver).options(selectinload(Driver.auto)).where(Driver.id == driver_id)
#     )
#     result: Result = await session.execute(stmt)
#
#     transport_unit_with_driver = result.scalars().one()
#     transport_units_with_id_autos = transport_unit_with_driver.auto
#     id_autos_list = [
#         transport_unit.auto_id for transport_unit in transport_units_with_id_autos
#     ]
#
#     stmt = select(Auto).where(Auto.id.in_(id_autos_list))
#     result: Result = await session.execute(stmt)
#     autos = result.scalars().all()
#
#     # ___through TransportUnit table___
#     # stmt = select(TransportUnit).options(selectinload(TransportUnit.user)).where(TransportUnit.driver_id == driver_id)
#     # result: Result = await session.execute(stmt)
#     #
#     # transport_units = result.scalars().all()
#     # autos = [transport_unit.user for transport_unit in transport_units]
#
#     return list(autos)
#
#
# async def get_all_driver_routes(session: AsyncSession, driver_id) -> list[Route]:
#     stmt = (
#         select(Driver).options(selectinload(Driver.auto)).where(Driver.id == driver_id)
#     )
#     result: Result = await session.execute(stmt)
#
#     transport_unit_with_driver = result.scalars().one()
#     transport_units_with_id_autos = transport_unit_with_driver.auto
#     id_transport_units = [
#         transport_unit.id for transport_unit in transport_units_with_id_autos
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
