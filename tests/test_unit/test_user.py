import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.crud import create_user
from api_v1.user.schemas import UserCreate
from core.config import settings
from core.models import User, db_helper
from main import app
from tests.utils import TestUserOk

client = TestClient(app)

prefix = settings.api_v1_prefix + settings.user_prefix


async def create_test_user(session: AsyncSession):
    user = UserCreate(
        vk_id=TestUserOk.vk_id,
        first_name=TestUserOk.first_name,
        last_name=TestUserOk.last_name,
        sex=TestUserOk.sex,
        city=TestUserOk.city,
        bdate=TestUserOk.bdate,
        vk_group=TestUserOk.vk_group,
        archived=TestUserOk.archived,
    )

    await create_user(session, user)
    await session.commit()


async def create_test_user_archived(session: AsyncSession):
    user = UserCreate(
        vk_id=TestUserOk.vk_id,
        first_name=TestUserOk.first_name,
        last_name=TestUserOk.last_name,
        sex=TestUserOk.sex,
        city=TestUserOk.city,
        bdate=TestUserOk.bdate,
        vk_group=TestUserOk.vk_group,
        archived=True,
    )

    await create_user(session, user)
    await session.commit()


async def delete_user_by_vk_id(session: AsyncSession):
    stmt = delete(User).where(User.vk_id == TestUserOk.vk_id)
    await session.execute(stmt)
    await session.commit()


async def get_user_by_vk_id(session: AsyncSession):
    stmt = select(User).where(User.vk_id == TestUserOk.vk_id)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


@pytest.mark.asyncio()
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


@pytest.mark.asyncio
# @pytest_asyncio.is_async_test
async def test_user_restore():
    async with db_helper.async_session_factory() as session:
        await create_test_user_archived(session)

        user_from_db = await get_user_by_vk_id(session)
        user_id = user_from_db.id

        response = client.patch(f"{prefix}/{user_id}/restore/")

        assert response.status_code == 200

        await delete_user_by_vk_id(session)
