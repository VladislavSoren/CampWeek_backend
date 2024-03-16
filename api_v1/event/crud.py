from datetime import datetime
from operator import and_

from pytz import timezone
from sqlalchemy import Result, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event.schemas import EventCreate, EventUpdatePartial
from api_v1.event.utils import EventActType
from core.models import Event


async def create_event(session: AsyncSession, event_in: EventCreate) -> Event:
    event = Event(**event_in.model_dump())
    session.add(event)
    await session.commit()
    # await session.refresh(product)
    return event


async def get_events(session: AsyncSession, actual_type, offset=0, limit=10, region_ids: str = None) -> list[Event]:
    current_time = datetime.now()
    current_time = current_time.astimezone(timezone("UTC"))

    if actual_type == EventActType.actual:
        filter_type = Event.date_time > current_time
    elif actual_type == EventActType.passed:
        filter_type = Event.date_time <= current_time
    else:
        filter_type = true()

    if region_ids:
        region_ids_list = region_ids.split(";")
        region_ids_list = [int(reg_id) for reg_id in region_ids_list]
        filter_reg = Event.region_id == region_ids_list[0]
        for region_id in region_ids_list[1:]:
            filter_reg = filter_reg | (Event.region_id == region_id)
    else:
        filter_reg = true()

    # Объединяем фильтры
    filters = filter_type & filter_reg

    stmt = select(Event).order_by(Event.date_time.asc(), Event.time_start.asc()).filter(filters)
    stmt = stmt.offset(offset).limit(limit)
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


async def get_events_by_creator_id(session: AsyncSession, creator_id, actual_type, offset, limit) -> list[Event] | None:
    current_time = datetime.now()
    current_time = current_time.astimezone(timezone("UTC"))

    if actual_type == EventActType.actual:
        filters = and_(
            Event.date_time > current_time,
            Event.creator_id == creator_id,
        )
    elif actual_type == EventActType.passed:
        filters = and_(
            Event.date_time <= current_time,
            Event.creator_id == creator_id,
        )
    else:
        filters = Event.creator_id == creator_id

    stmt = select(Event).order_by(Event.date_time.asc(), Event.time_start.asc()).filter(filters)
    stmt = stmt.offset(offset).limit(limit)
    result: Result = await session.execute(stmt)
    events = result.scalars().all()

    return list(events)


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
