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


async def get_events(session: AsyncSession, actual_type, offset, limit, approved, region_ids) -> list[Event]:
    current_time = datetime.now()
    current_time = current_time.astimezone(timezone("UTC"))

    # Фильтр актуальности события
    if actual_type == EventActType.actual:
        filter_type = Event.date_time > current_time
    elif actual_type == EventActType.passed:
        filter_type = Event.date_time <= current_time
    else:
        filter_type = true()

    # Фильтр по approved
    if approved is not None:
        filter_approved = Event.approved == approved
    else:
        filter_approved = true()

    # Фильтр по регионам
    if region_ids:
        region_ids_list = region_ids.split(";")
        region_ids_list = [int(reg_id) for reg_id in region_ids_list]
        filter_reg = Event.region_id == region_ids_list[0]
        for region_id in region_ids_list[1:]:
            filter_reg = filter_reg | (Event.region_id == region_id)
    else:
        filter_reg = true()

    # Объединяем фильтры
    filters = filter_type & filter_reg & filter_approved

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
