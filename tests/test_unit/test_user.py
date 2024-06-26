import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from api_v1.user.crud import create_user
from api_v1.user.schemas import UserCreate
from core.config import settings
from core.models import User, db_helper
from main import app
from tests.utils import TestUserOk

client = TestClient(app)

prefix = settings.user_prefix


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


# @pytest_asyncio.fixture(scope="function")
# async def create_and_delete_user_in_db():
#     # Точка ДО выполнения теста
#     async with db_helper.async_session_factory() as session:
#         user = UserCreate(
#             vk_id=TestUserOk.vk_id,
#             first_name=TestUserOk.first_name,
#             last_name=TestUserOk.last_name,
#             sex=TestUserOk.sex,
#             city=TestUserOk.city,
#             bdate=TestUserOk.bdate,
#             vk_group=TestUserOk.vk_group,
#             archived=True,
#         )
#
#         await create_user(session, user_in=user)
#
#     # Точка, где выполняется тест
#     yield
#
#     # Очистка данных после теста
#     # async with db_helper.async_session_factory() as session:
#
#     session = db_helper.scoped_session_dependency()
#
#     stmt = delete(User).where(User.vk_id == TestUserOk.vk_id)
#     await session.execute(stmt)
#     await session.commit()
#
#     await session.close()


# @pytest.mark.asyncio()
# async def test_create_user(delete_created_user_in_db):
#     async with db_helper.async_session_factory() as session:
#         user = UserCreate(
#             vk_id=TestUserOk.vk_id,
#             first_name=TestUserOk.first_name,
#             last_name=TestUserOk.last_name,
#             sex=TestUserOk.sex,
#             city=TestUserOk.city,
#             bdate=TestUserOk.bdate,
#             vk_group=TestUserOk.vk_group,
#             archived=TestUserOk.archived,
#         )
#
#         await create_user(session, user_in=user)
#
#         stmt = select(User).where(User.vk_id == TestUserOk.vk_id)
#         result: Result = await session.execute(stmt)
#         user_from_db = result.scalars().one()
#
#         # Преобразуем его в экземпляр TestUserOk
#         test_user = TestUserOk(
#             vk_id=user_from_db.vk_id,
#                 first_name=user_from_db.first_name,
#             last_name=user_from_db.last_name,
#             sex=user_from_db.sex,
#             city=user_from_db.city,
#             bdate=user_from_db.bdate,
#             vk_group=user_from_db.vk_group,
#             archived=user_from_db.archived,
#         )
#
#         assert test_user == TestUserOk()
#
#
# @pytest.mark.asyncio
# async def test_read_main(create_and_delete_user_in_db):
#     async with db_helper.async_session_factory() as session:
#         stmt = select(User).where(User.vk_id == TestUserOk.vk_id)
#         result: Result = await session.execute(stmt)
#         user_from_db = result.scalars().one()
#         user_id = user_from_db.id
#
#         # response_user_by_id = client.patch(prefix + f"/{user_id}/restore/")
#
#         # Отправляем PATCH запрос
#         # response = client.patch(f"{prefix}/{user_id}/restore/")
#
#     response = client.patch(f"http://127.0.0.1:5777/api/v1/user/{user_id}/restore/")
#     # http://127.0.0.1:5777/api/v1/user/27/restore/
#
#     # Проверяем код ответа
#     assert response.status_code == 200
#
#     pass


@pytest_asyncio.fixture(scope="function")
async def create_and_delete_user_in_db():
    # Создание пользователя в базе данных
    async with db_helper.async_session_factory() as session:
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

    # # Передача управления тесту
    # yield
    #
    # # await session.close()
    #
    # # Очистка данных после теста
    # async with db_helper.async_session_factory() as session:
    #     stmt = delete(User).where(User.vk_id == TestUserOk.vk_id)
    #     await session.execute(stmt)
    #     await session.commit()


# @pytest_asyncio.fixture(scope="function")
# async def delete_user_in_db(request):
#     async def delete_user():
#         async with db_helper.async_session_factory() as session:
#             stmt = delete(User).where(User.vk_id == TestUserOk.vk_id)
#             await session.execute(stmt)
#             await session.commit()
#
#     request.addfinalizer(delete_user)


async def delete_user_by_vk_id(session):
    stmt = delete(User).where(User.vk_id == TestUserOk.vk_id)
    await session.execute(stmt)
    await session.commit()


async def get_user_by_vk_id(session):
    stmt = select(User).where(User.vk_id == TestUserOk.vk_id)
    result = await session.execute(stmt)
    return result.scalars().one()


@pytest.mark.asyncio
# @pytest_asyncio.is_async_test
async def test_read_main():
    async with db_helper.async_session_factory() as session:
        # stmt = select(User).where(User.vk_id == TestUserOk.vk_id)
        # result = await session.execute(stmt)
        # user_from_db = result.scalars().one()
        user_from_db = await get_user_by_vk_id(session)
        user_id = user_from_db.id

        response = client.patch(f"/api/v1/user/{user_id}/restore/")

        assert response.status_code == 200

        await delete_user_by_vk_id(session)
