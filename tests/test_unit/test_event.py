import json
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from api_v1.event.schemas import EventCreate
from core.config import settings
from core.models import db_helper
from main import app
from tests.utils import (
    TestEventOk,
    create_region_test,
    create_role_admin_test,
    create_test_event_for_all_tests,
    create_test_event_for_one_test,
    create_test_user,
    create_userrole_admin_test,
    delete_event_by_name_for_all_tests,
    delete_event_by_name_for_one_test,
    delete_region_test,
    delete_role_admin_test,
    delete_user_by_vk_id,
    delete_userrole_admin_test,
    get_event_by_name_for_one_test,
    get_region_by_name_test,
    get_user_by_vk_id,
)

client = TestClient(app)

prefix = settings.api_v1_prefix + settings.event_prefix
base_test_url = "http://test"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_setup_session():
    # Before all module tests
    async with db_helper.async_session_factory() as session:
        # Создаём тестового юзера
        await create_test_user(session)

        # Создаём регион
        await create_region_test(session)

        # Создаём тестовое событие
        await create_test_event_for_all_tests(session)

        # Создаём тестовую роль admin
        await create_role_admin_test(session)

        # Присваиваем юзеру роль admin
        await create_userrole_admin_test(session)

    yield
    # After all module tests
    async with db_helper.async_session_factory() as session:
        await delete_userrole_admin_test(session)

        await delete_role_admin_test(session)

        await delete_event_by_name_for_all_tests(session)

        await delete_region_test(session)

        await delete_user_by_vk_id(session)


# Проверка восстановления архивного юзера
@pytest.mark.asyncio(scope="session")
async def test_create_event():
    async with db_helper.async_session_factory() as session:
        user_id = (await get_user_by_vk_id(session)).id
        region_id = (await get_region_by_name_test(session)).id

        event = EventCreate(
            name=TestEventOk.name_for_one_test,
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
            region_id=region_id,
            creator_id=user_id,
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
        assert event_response["name"] == TestEventOk.name_for_one_test

        # Чисти базу от тестовых данных
        await delete_event_by_name_for_one_test(session)


# Проверка восстановления архивного юзера
@pytest.mark.asyncio(scope="session")
async def test_get_event():
    async with db_helper.async_session_factory() as session:
        await create_test_event_for_one_test(session)

        # Получаем id созданного юзера
        event_id = (await get_event_by_name_for_one_test(session)).id

        # Получаем словарь с атрибутами юзера
        async with AsyncClient(app=app, base_url=base_test_url) as ac:
            response = await ac.get(f"{prefix}/{event_id}/")
        json_string = response.content.decode("utf-8")
        event_response = json.loads(json_string)

        # Проверки
        assert response.status_code == 200
        assert event_response["id"] == event_id

        # Чисти базу от тестовых данных
        await delete_event_by_name_for_one_test(session)


# # async def create
# @pytest.mark.asyncio(scope="session")
# async def test_approve_event():
#     async with db_helper.async_session_factory() as session:
#         # Создаём архивного юзера
#         await create_test_event(session)
#
#         # Получаем id созданного юзера
#         event_id = (await get_event_by_name(session)).id
#
#         # Подготовка заголовков
#
#         # Подготовка данных
#         event_data = {"approved": True}
#         token = "Bearer " + create_access_token(user_id=1)
#         headers = {"Authorization": token}  # временно хардкорно TestUserOk
#
#         # Получаем словарь с атрибутами юзера
#         async with AsyncClient(app=app, base_url=base_test_url) as ac:
#             response = await ac.patch(f"{prefix}/{event_id}/approve/", json=event_data, headers=headers)
#         json_string = response.content.decode("utf-8")
#         event_response = json.loads(json_string)
#
#         # Проверки
#         assert response.status_code == 200
#         assert event_response["id"] == event_id
#
#         # Чисти базу от тестовых данных
#         await delete_event_by_name(session)
