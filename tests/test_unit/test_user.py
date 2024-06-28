import json

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from core.config import settings
from core.models import db_helper
from main import app
from tests.utils import (
    TestUserOk,
    create_test_user,
    create_test_user_archived,
    delete_user_by_vk_id,
    get_user_by_vk_id,
)

client = TestClient(app)

prefix = settings.api_v1_prefix + settings.user_prefix
base_test_url = "http://test"


@pytest.mark.asyncio(scope="session")
# @pytest.mark.asyncio
async def test_create_user():
    async with db_helper.async_session_factory() as session:
        await create_test_user(session)

        user_from_db = await get_user_by_vk_id(session)

        # Преобразуем его в экземпляр TestUserOk
        test_user = TestUserOk()
        test_user_from_db = TestUserOk(
            vk_id=user_from_db.vk_id,
            first_name=user_from_db.first_name,
            last_name=user_from_db.last_name,
            sex=user_from_db.sex,
            city=user_from_db.city,
            bdate=user_from_db.bdate,
            vk_group=user_from_db.vk_group,
            archived=user_from_db.archived,
        )

        await delete_user_by_vk_id(session)

        assert test_user == test_user_from_db


# Проверка восстановления архивного юзера
@pytest.mark.asyncio(scope="session")
async def test_get_user():
    async with db_helper.async_session_factory() as session:
        # Создаём архивного юзера
        await create_test_user(session)

        # Получаем id созданного юзера
        user_id = (await get_user_by_vk_id(session)).id

        # Получаем словарь с атрибутами юзера
        async with AsyncClient(app=app, base_url=base_test_url) as ac:
            response = await ac.get(f"{prefix}/{user_id}/")
        json_string = response.content.decode("utf-8")
        user_response = json.loads(json_string)

        # Проверки
        assert response.status_code == 200
        assert user_response["id"] == user_id

        # Чисти базу от тестовых данных
        await delete_user_by_vk_id(session)


# Проверка восстановления архивного юзера
@pytest.mark.asyncio(scope="session")
# @pytest.mark.asyncio
async def test_user_restore():
    async with db_helper.async_session_factory() as session:
        # Создаём архивного юзера
        await create_test_user_archived(session)

        # Получаем id созданного юзера
        user_id = (await get_user_by_vk_id(session)).id

        # Получаем словарь с атрибутами юзера
        async with AsyncClient(app=app, base_url=base_test_url) as ac:
            response = await ac.patch(f"{prefix}/{user_id}/restore/")
        json_string = response.content.decode("utf-8")
        user_response = json.loads(json_string)

        # Проверки
        assert response.status_code == 200
        assert user_response["archived"] is False

        # Чисти базу от тестовых данных
        await delete_user_by_vk_id(session)


# Проверка удаления (архивирования) юзера
@pytest.mark.asyncio(scope="session")
# @pytest.mark.asyncio
async def test_user_archive():
    async with db_helper.async_session_factory() as session:
        # Создаём архивного юзера
        await create_test_user(session)

        # Получаем id созданного юзера
        user_id = (await get_user_by_vk_id(session)).id

        # Получаем словарь с атрибутами юзера
        async with AsyncClient(app=app, base_url=base_test_url) as ac:
            response = await ac.delete(f"{prefix}/{user_id}/delete/")
        json_string = response.content.decode("utf-8")
        user_response = json.loads(json_string)

        # получаем архивированного юзера из БД
        user_from_db = await get_user_by_vk_id(session)

        # Проверки
        assert response.status_code == 200
        assert str(user_id) in user_response["msg"]
        assert user_from_db.archived is True

        # Чисти базу от тестовых данных
        await delete_user_by_vk_id(session)
