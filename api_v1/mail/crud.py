"""
Two mailings:
- any_days_before
- any_hours_minutes_before

*any_days_before
- if days_shift NOT None or 0
- Get events from DB which will start in set days_shift
- Make task for mailing
- Set standard mailing time

*any_hours_minutes_before
- if days_shift is None or 0
- Get today events from DB
- Make task for mailing for every event
- Set tyme by hours_shift & minutes_shift
"""
from datetime import datetime, timedelta

import vk_api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException
# from sqlalchemy import Result, select
from sqlalchemy import Result, select, update, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from api_v1.event.crud import get_actual_events
from api_v1.eventvisitor.crud import get_event_visitors_id_set
from api_v1.mail.schemas import AutoEventMailCreate, AutoEventMailUpdatePartial
from api_v1.user.crud import get_users
from core.config import ACCESS_MESSAGE_GROUP_TOKEN
from core.models import AutoEventMail, db_helper, Event, User
from init_global_shedular import global_scheduler


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


async def make_manual_mailing(session, event_mail_task, any_registered):
    global_scheduler.print_jobs()

    users_registered_set = set()

    # async with db_helper.async_session_factory() as session:

    # Получаем всех НЕ удалённых юзеров
    users_all_not_archived = await get_users(session)

    # Получаем все АКТУАЛЬНЫЕ и НЕ удалённые события
    events = await get_actual_events(session)

    # Формируем кортеж юзеров, которые зарегестрированы хотя бы на одно событие
    for user in users_all_not_archived:
        for event in events:
            users_id_set = await get_event_visitors_id_set(session, event.id)

            if user.id in users_id_set:
                users_registered_set.add(user)
                break

    if not any_registered:
        users_for_mail = set(users_all_not_archived) - users_registered_set
    else:
        users_for_mail = users_registered_set

    # При выставленном флаге send_now - осуществляется мгноаенная рассылка
    # При send_datetime - рассылка по указынной дате и времени
    if event_mail_task.send_now and event_mail_task.send_datetime is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only one field must be filled",
        )

    if event_mail_task.send_now:
        await send_mail_by_users(users_for_mail)
    else:
        if event_mail_task.send_datetime is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"One of the fields must be filled",
            )
        else:
            task_execute_date = event_mail_task.send_datetime.strftime("%Y-%m-%d %H:%M:%S")
            global_scheduler.add_job(
                send_mail_by_users,
                args=[users_for_mail], trigger='date',
                run_date=task_execute_date,
                misfire_grace_time=60,  # sec
                id=f'manual_{task_execute_date}',
                replace_existing=True,
            )
            global_scheduler.print_jobs()

    # current_time = datetime.now()
    # task_execute_date = (current_time + timedelta(
    #     minutes=1
    # ))


async def send_mail_by_users(users):
    print("send_mail_by_users_id(users_id)")

    current_time = datetime.now()

    token = ACCESS_MESSAGE_GROUP_TOKEN
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    for user in users:

        message = f"first_name - {user.first_name}\nlast_name - {user.last_name}\n"
        message = f"{message}\nВремя отправления - {current_time}"

        user_id = user.vk_id

        random_id = 0
        try:
            response = vk.messages.send(
                user_id=user_id,
                random_id=random_id,
                message=message,
            )
        except vk_api.exceptions.ApiError as e:
            print(e)