# from sqlalchemy import Result, select
from sqlalchemy import Result, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.mail.schemas import AutoEventMailCreate, AutoEventMailUpdatePartial
from core.models import AutoEventMail


# from sqlalchemy.orm import selectinload


class ExistStatus:
    EXISTS = "exists"
    NEW = "new"


async def create_auto_event_mail(session: AsyncSession, auto_event_mail_in: AutoEventMailCreate) -> AutoEventMail | str:
    auto_event_mail = AutoEventMail(**auto_event_mail_in.model_dump())
    session.add(auto_event_mail)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "UniqueViolationError" in e.args[0]:
            return ExistStatus.EXISTS
    finally:
        await session.close()
    # await session.refresh(product)
    return auto_event_mail


async def get_auto_event_mails(session: AsyncSession) -> list[AutoEventMail]:
    stmt = select(AutoEventMail).order_by(AutoEventMail.id).where(AutoEventMail.archived.is_(False))
    result: Result = await session.execute(stmt)
    auto_event_mails = result.scalars().all()
    return list(auto_event_mails)


async def get_all_auto_event_mails(session: AsyncSession) -> list[AutoEventMail]:
    stmt = select(AutoEventMail).order_by(AutoEventMail.id)
    result: Result = await session.execute(stmt)
    auto_event_mails = result.scalars().all()
    return list(auto_event_mails)


async def get_auto_event_mail(session: AsyncSession, auto_event_mail_id) -> AutoEventMail | None:
    return await session.get(AutoEventMail, auto_event_mail_id)


async def update_auto_event_mail(
        auto_event_mail_update: AutoEventMailUpdatePartial,
        auto_event_mail: AutoEventMail,
        session: AsyncSession,
        partial: bool = False,
) -> AutoEventMail | None:
    # обновляем атрибуты
    for name, value in auto_event_mail_update.model_dump(exclude_unset=partial).items():
        setattr(auto_event_mail, name, value)
    await session.commit()

    return auto_event_mail


async def archive_auto_event_mail(session: AsyncSession, auto_event_mail_id):
    stmt = update(AutoEventMail).where(AutoEventMail.id == auto_event_mail_id).values(archived=True)
    await session.execute(stmt)
    await session.commit()


async def restore_auto_event_mail(session: AsyncSession, auto_event_mail_id):
    stmt = update(AutoEventMail).where(AutoEventMail.id == auto_event_mail_id).values(archived=False)
    await session.execute(stmt)
    await session.commit()
