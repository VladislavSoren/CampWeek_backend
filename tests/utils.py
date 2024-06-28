from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.event.crud import create_event
from api_v1.event.schemas import EventCreate
from api_v1.region.crud import create_region
from api_v1.region.schemas import RegionCreate
from api_v1.role.crud import create_role
from api_v1.role.schemas import RoleCreate
from api_v1.user.crud import create_user
from api_v1.user.schemas import UserCreate
from api_v1.userrole.crud import create_userrole
from api_v1.userrole.schemas import UserRoleCreate
from core.models import Event, Region, Role, User, UserRole


@dataclass
class TestUserOk:
    __test__ = False
    vk_id: str = "1234554321"
    vk_id_for_one_test: str = "vk_id_for_one_test"
    first_name: str = "1"
    last_name: str = "1"
    sex: int = 1
    city: str = "1"
    bdate: datetime.date = datetime.now().date()
    vk_group: str = "1"
    archived: bool = False


@dataclass
class TestEventOk:
    __test__ = False
    name_for_one_test: str = "TestEventOkOne"
    name_for_all_tests: str = "TestEventOkAll"
    link: str = "1"
    add_link: str = "1"
    date_time: datetime = datetime.now()
    time_start: str = "12:00"

    time_end: str = "13:00"
    is_reg_needed: bool = True
    approved: bool = False
    description: str = "1"
    add_info: str = "1"

    notes: str = "1"
    roles: str = "1"
    region_id: int = 1
    creator_id: int = 1


@dataclass
class TestRoleOk:
    __test__ = False
    name_admin: str = "admin_test"
    archived: bool = False


@dataclass
class RegionOk:
    __test__ = False
    name: str = "region_test"
    archived: bool = False


@dataclass
class TestUserRoleAdminOk:
    __test__ = False
    user_id: int
    role_id: int


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


async def create_test_user_for_one_test(session: AsyncSession):
    user = UserCreate(
        vk_id=TestUserOk.vk_id_for_one_test,
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


async def delete_user_by_vk_id_for_one_test(session: AsyncSession):
    stmt = delete(User).where(User.vk_id == TestUserOk.vk_id_for_one_test)
    await session.execute(stmt)
    await session.commit()


async def get_user_by_vk_id_for_one_test(session: AsyncSession):
    stmt = select(User).where(User.vk_id == TestUserOk.vk_id_for_one_test)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


async def create_test_event_for_one_test(session: AsyncSession):
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
    await create_event(session, event)
    await session.commit()


async def delete_event_by_name_for_one_test(session: AsyncSession):
    stmt = delete(Event).where(Event.name == TestEventOk.name_for_one_test)
    await session.execute(stmt)
    await session.commit()


async def get_event_by_name_for_one_test(session: AsyncSession):
    stmt = select(Event).where(Event.name == TestEventOk.name_for_one_test)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


async def create_test_event_for_all_tests(session):
    user_id = (await get_user_by_vk_id(session)).id
    region_id = (await get_region_by_name_test(session)).id

    event = EventCreate(
        name=TestEventOk.name_for_all_tests,
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

    await create_event(session, event)


async def delete_event_by_name_for_all_tests(session: AsyncSession):
    stmt = delete(Event).where(Event.name == TestEventOk.name_for_all_tests)
    await session.execute(stmt)
    await session.commit()


async def get_event_by_name_for_all_tests(session: AsyncSession):
    stmt = select(Event).where(Event.name == TestEventOk.name_for_all_tests)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


async def create_role_admin_test(session: AsyncSession):
    role = RoleCreate(name=TestRoleOk.name_admin, archived=TestRoleOk.archived)
    await create_role(session, role)


async def get_role_by_name_test(session: AsyncSession):
    stmt = select(Role).where(Role.name == TestRoleOk.name_admin)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


async def create_userrole_admin_test(session: AsyncSession):
    user_id = (await get_user_by_vk_id(session)).id
    role_id = (await get_role_by_name_test(session)).id
    user_role = UserRoleCreate(user_id=user_id, role_id=role_id)
    await create_userrole(session, user_role)


async def delete_userrole_admin_test(session: AsyncSession):
    user_id = (await get_user_by_vk_id(session)).id
    stmt = delete(UserRole).where(UserRole.user_id == user_id)
    await session.execute(stmt)
    await session.commit()


async def delete_role_admin_test(session: AsyncSession):
    stmt = delete(Role).where(Role.name == TestRoleOk.name_admin)
    await session.execute(stmt)
    await session.commit()


async def create_region_test(session: AsyncSession):
    role = RegionCreate(name=RegionOk.name, archived=RegionOk.archived)
    await create_region(session, role)


async def get_region_by_name_test(session: AsyncSession):
    stmt = select(Region).where(Region.name == RegionOk.name)
    result: Result = await session.execute(stmt)
    return result.scalars().one()


async def delete_region_test(session: AsyncSession):
    stmt = delete(Region).where(Region.name == RegionOk.name)
    await session.execute(stmt)
    await session.commit()
