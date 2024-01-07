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


async def create_auto_event_mail(session: AsyncSession, auto_event_mail_in: AutoEventMailCreate) -> str:
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
    return ExistStatus.NEW


async def get_auto_event_mails(session: AsyncSession) -> list[AutoEventMail]:
    stmt = select(AutoEventMail).order_by(AutoEventMail.id).where(AutoEventMail.archived.is_(False))
    result: Result = await session.execute(stmt)
    auto_event_mails = result.scalars().all()
    return list(auto_event_mails)

# async def get_all_users(session: AsyncSession) -> list[User]:
#     stmt = select(User).order_by(User.id)
#     result: Result = await session.execute(stmt)
#     users = result.scalars().all()
#     return list(users)
# 
#
# 
# 
# async def get_user(session: AsyncSession, user_id) -> User | None:
#     return await session.get(User, user_id)
# 
# 
# async def get_user_by_vk_id(session: AsyncSession, user_vk_id) -> User | None:
#     stmt = select(User).where(User.vk_id == user_vk_id)
#     result: Result = await session.execute(stmt)
#     user = result.scalars().one()
#     return user
# 
# 
# async def update_user(
#         user_update: UserUpdatePartial,
#         user: User,
#         session: AsyncSession,
#         partial: bool = False,
# ) -> User | None:
#     # обновляем атрибуты
#     for name, value in user_update.model_dump(exclude_unset=partial).items():
#         if name != "vk_id":
#             setattr(user, name, value)
#     await session.commit()
# 
#     return user
# 
# 
# async def archive_user(session: AsyncSession, user_id):
#     stmt = update(User).where(User.id == user_id).values(archived=True)
#     await session.execute(stmt)
#     await session.commit()
# 
# 
# async def restore_user(session: AsyncSession, user_id):
#     stmt = update(User).where(User.id == user_id).values(archived=False)
#     await session.execute(stmt)
#     await session.commit()
