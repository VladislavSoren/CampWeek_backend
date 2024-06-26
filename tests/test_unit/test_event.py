import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event.crud import create_event
from api_v1.event.schemas import EventCreate
from core.config import settings
from core.models import Event, db_helper
from main import app
from tests.utils import TestEventOk

client = TestClient(app)

prefix = settings.api_v1_prefix + settings.event_prefix
base_test_url = "http://test"


async def create_test_event(session: AsyncSession):
    event = EventCreate(
        name=TestEventOk.name,
        link=TestEventOk.link,
        add_link=TestEventOk.add_link,
        date_time=TestEventOk.date_time,
        time_start=TestEventOk.time_start,
        time_end=TestEventOk.time_end,
        is_reg_needed=TestEventOk.is_reg_needed,
        approved=TestEventOk.approved,
        description=TestEventOk.description,
        add_info=TestEventOk.add_info,
        notes=TestEventOk.notes,
        roles=TestEventOk.roles,
        region_id=TestEventOk.region_id,
        creator_id=TestEventOk.creator_id,
    )

    await create_event(session, event)
    await session.commit()


async def delete_event_by_name(session: AsyncSession):
    stmt = delete(Event).where(Event.name == TestEventOk.name)
    await session.execute(stmt)
    await session.commit()


async def get_event_by_name(session: AsyncSession):
    stmt = select(Event).where(Event.name == TestEventOk.name)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


# Проверка восстановления архивного юзера
@pytest.mark.asyncio(scope="session")
async def test_create_event():
    async with db_helper.async_session_factory() as session:
        event = EventCreate(
            name=TestEventOk.name,
            link=TestEventOk.link,
            add_link=TestEventOk.add_link,
            date_time=TestEventOk.date_time,
            time_start=TestEventOk.time_start,
            time_end=TestEventOk.time_end,
            is_reg_needed=TestEventOk.is_reg_needed,
            approved=TestEventOk.approved,
            description=TestEventOk.description,
            add_info=TestEventOk.add_info,
            notes=TestEventOk.notes,
            roles=TestEventOk.roles,
            region_id=TestEventOk.region_id,
            creator_id=TestEventOk.creator_id,
        )

        # Convert the event to a dictionary and ensure datetime objects are serialized
        event_data = event.model_dump()
        for key, value in event_data.items():
            if isinstance(value, datetime):
                event_data[key] = value.isoformat()

        # Получаем словарь с атрибутами юзера
        async with AsyncClient(app=app, base_url=base_test_url) as ac:
            response = await ac.post(f"{prefix}/", json=event_data)
        json_string = response.content.decode("utf-8")
        event_response = json.loads(json_string)

        # Проверки
        assert response.status_code == 201
        assert event_response["name"] == TestEventOk.name

        # Чисти базу от тестовых данных
        await delete_event_by_name(session)


# Проверка восстановления архивного юзера
@pytest.mark.asyncio(scope="session")
async def test_get_event():
    async with db_helper.async_session_factory() as session:
        # Создаём архивного юзера
        await create_test_event(session)

        # Получаем id созданного юзера
        event_id = (await get_event_by_name(session)).id

        # Получаем словарь с атрибутами юзера
        async with AsyncClient(app=app, base_url=base_test_url) as ac:
            response = await ac.get(f"{prefix}/{event_id}/")
        json_string = response.content.decode("utf-8")
        event_response = json.loads(json_string)

        # Проверки
        assert response.status_code == 200
        assert event_response["id"] == event_id

        # Чисти базу от тестовых данных
        await delete_event_by_name(session)
