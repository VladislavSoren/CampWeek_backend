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
from datetime import datetime

import vk_api

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException

# from sqlalchemy import Result, select
from sqlalchemy import Result, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.event.crud import get_events
from api_v1.event.utils import EventActType
from api_v1.eventvisitor.crud import get_event_visitors_id_set
from api_v1.mail.schemas import AutoEventMailCreate, AutoEventMailUpdatePartial
from api_v1.user.crud import get_users
from core.crypto import decrypt_message, load_key
from core.models import AutoEventMail, GroupVK, User, db_helper
from init_global_shedular import global_scheduler

# from sqlalchemy.orm import selectinload


class CustomVkApi(vk_api.VkApi):
    def __init__(self, group_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = group_name

    def get_group_name(self):
        return self.group_name


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

    # Получаем всех НЕ удалённых юзеров
    users_all_not_archived = await get_users(session)

    # Получаем все АКТУАЛЬНЫЕ и НЕ удалённые события
    events = await get_events(session, actual_type=EventActType.actual)

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
            detail="Only one field must be filled",
        )

    if event_mail_task.send_now:
        await send_mail_by_users(users_for_mail)
    else:
        if event_mail_task.send_datetime is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="One of the fields must be filled",
            )
        else:
            task_execute_date = event_mail_task.send_datetime.strftime("%Y-%m-%d %H:%M:%S")
            global_scheduler.add_job(
                send_mail_by_users,
                args=[users_for_mail],
                trigger="date",
                run_date=task_execute_date,
                misfire_grace_time=60,  # sec
                id=f"manual_{task_execute_date}",
                replace_existing=True,
            )
            global_scheduler.print_jobs()


async def send_mail_by_users(target_users=None):
    # Получаем множество vk_id целевой аудитории для сравнения с выборками из БД
    target_users_id = {obj.vk_id for obj in target_users}

    async with db_helper.async_session_factory() as session:
        # Подгружаем ключ для расшифровки токенов
        key = load_key()

        # получаем токены из БД
        stmt = select(GroupVK)
        result: Result = await session.execute(stmt)
        groups = result.scalars().all()

        session_users_dict = {}
        for group in groups:
            # Получаем всех юзеров группы с данным токеном
            stmt = select(User).where(User.vk_group == group.name)
            result: Result = await session.execute(stmt)
            users = result.scalars().all()

            # Если на вход были поданы целевые юзеры -> находим целевых входящих в текущую группу
            if target_users:
                users_id = {obj.vk_id for obj in users}
                users_id_union = target_users_id & users_id
                users = {obj for obj in users if obj.vk_id in users_id_union}

            # Создаём объект API VK в рамках сессии текущего токена
            token_decrypt = decrypt_message(group.token, key)
            vk_session = CustomVkApi(token=token_decrypt, group_name=group.name)

            # Наполняем словарь "сессия": "юзеры"
            session_users_dict[vk_session] = users

        # Делаем рассылку по группам юзеров в рамках "подходящих" для них сессий
        for vk_session, users in session_users_dict.items():
            vk = vk_session.get_api()

            # Проходимся по всем юзерам в рамках "актуальной" для него группы
            for user in users:
                # if user.vk_group == None:
                user_id = user.vk_id

                current_time = datetime.now()
                message = f"first_name - {user.first_name}\nlast_name - {user.last_name}\n"
                message = f"{message}\nВремя отправления - {current_time}"

                random_id = 0
                try:
                    vk.messages.send(
                        user_id=user_id,
                        random_id=random_id,
                        message=message,
                    )
                except vk_api.exceptions.ApiError as e:
                    print(e)  # [5] User authorization failed: invalid access_token (4).
                    for vk_session_loc in session_users_dict.keys():
                        vk_loc = vk_session_loc.get_api()

                        try:
                            vk_loc.messages.send(
                                user_id=user_id,
                                random_id=random_id,
                                message=message,
                            )
                            # Записываем юзеру токен данной сессии
                            user.vk_group = vk_session_loc.get_group_name()

                        except vk_api.exceptions.ApiError as e:
                            print(e)
                            user.vk_group = None
                            continue
                        finally:
                            await session.commit()

        # получаем юзеров без токенов
        stmt = select(User).where(User.vk_group == None)
        result: Result = await session.execute(stmt)
        users = result.scalars().all()

        # Если на вход были поданы целевые юзеры
        if target_users:
            users_id = {obj.vk_id for obj in users}
            users_id_union = target_users_id & users_id
            users = {obj for obj in users if obj.vk_id in users_id_union}

        for vk_session_loc in session_users_dict.keys():
            vk_loc = vk_session_loc.get_api()

            # Несколькими сессиями проходимся по одной кучке юзеров
            for user in users:
                user_id = user.vk_id

                # И скипаем те которым проставились группы
                if user.vk_group == None:
                    current_time = datetime.now()
                    message = f"first_name - {user.first_name}\nlast_name - {user.last_name}\n"
                    message = f"{message}\nВремя отправления - {current_time}"

                    random_id = 0

                    try:
                        vk_loc.messages.send(
                            user_id=user_id,
                            random_id=random_id,
                            message=message,
                        )
                        # Записываем юзеру токен данной сессии
                        user.vk_group = vk_session_loc.get_group_name()

                    except vk_api.exceptions.ApiError as e:
                        print(e)
                        user.vk_group = None
                        continue
                    finally:
                        await session.commit()
