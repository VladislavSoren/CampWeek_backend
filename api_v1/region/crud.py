from sqlalchemy import Result, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.region.schemas import RegionCreate
from core.models import Region


class ExistStatus:
    EXISTS = "exists"
    NEW = "new"


async def create_region(session: AsyncSession, region_in: RegionCreate) -> Region | str:
    region = Region(**region_in.model_dump())
    session.add(region)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "UniqueViolationError" in e.args[0]:
            return ExistStatus.EXISTS
    finally:
        await session.close()
    return region


async def get_regions(session: AsyncSession) -> list[Region]:
    stmt = select(Region).order_by(Region.id).where(Region.archived.is_(False))
    result: Result = await session.execute(stmt)
    regions = result.scalars().all()
    return list(regions)


async def get_region(session: AsyncSession, region_id) -> Region | None:
    return await session.get(Region, region_id)


async def delete_obj(session: AsyncSession, region_id):
    stmt = (
        delete(Region)
        .where(
            Region.id == region_id,
        )
        .returning(Region.id)
    )
    deleted_obj_id = await session.execute(stmt)
    await session.commit()
    return deleted_obj_id
