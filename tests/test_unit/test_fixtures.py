import pytest_asyncio

from core.models import db_helper
from tests.utils import (
    create_region_test,
    create_role_admin_test,
    create_test_event_for_all_tests,
    create_test_user,
    create_userrole_admin_test,
    delete_event_by_name_for_all_tests,
    delete_region_test,
    delete_role_admin_test,
    delete_user_by_vk_id,
    delete_userrole_admin_test,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_setup_session():
    db_creations_list = [
        create_test_user,
        create_region_test,
        create_test_event_for_all_tests,
        create_role_admin_test,
        create_userrole_admin_test,
    ]

    db_deletions_list = [
        delete_userrole_admin_test,
        delete_role_admin_test,
        delete_event_by_name_for_all_tests,
        delete_region_test,
        delete_user_by_vk_id,
    ]

    # Before all module tests
    async with db_helper.async_session_factory() as session:
        for db_function in db_creations_list:
            await db_function(session)

    yield
    # After all module tests
    async with db_helper.async_session_factory() as session:
        for db_function in db_deletions_list:
            await db_function(session)


print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
