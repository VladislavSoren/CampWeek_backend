import pytest
import pytest_asyncio
from sqlalchemy import Result, delete, select

from api_v1.user.crud import create_user
from api_v1.user.schemas import UserCreate
from core.models import User, db_helper
from tests.utils import TestUserOk


@pytest_asyncio.fixture(scope="function")
async def delete_created_user_in_db():
    # Точка ДО выполнения теста

    # Точка, где выполняется тест
    yield

    # Очистка данных после теста
    async with db_helper.async_session_factory() as session:
        stmt = delete(User).where(User.vk_id == TestUserOk.vk_id)
        await session.execute(stmt)
        await session.commit()


@pytest.mark.asyncio()
async def test_create_user(delete_created_user_in_db):
    async with db_helper.async_session_factory() as session:
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

        await create_user(session, user_in=user)

        stmt = select(User).where(User.vk_id == TestUserOk.vk_id)
        result: Result = await session.execute(stmt)
        user_from_db = result.scalars().one()

        # Преобразуем его в экземпляр TestUserOk
        test_user = TestUserOk(
            vk_id=user_from_db.vk_id,
            first_name=user_from_db.first_name,
            last_name=user_from_db.last_name,
            sex=user_from_db.sex,
            city=user_from_db.city,
            bdate=user_from_db.bdate,
            vk_group=user_from_db.vk_group,
            archived=user_from_db.archived,
        )

        assert test_user == TestUserOk()
