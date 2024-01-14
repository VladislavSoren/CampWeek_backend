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
from sqlalchemy import select, Result, and_
from sqlalchemy.orm import selectinload

from api_v1.mail import crud
from core.config import ACCESS_MESSAGE_GROUP_TOKEN
from core.models import db_helper, Event, User
from init_global_shedular import global_scheduler


async def get_events_by_date(days_shift):
    print("get_events_by_date")
    async with db_helper.async_session_factory() as session:
        current_time = datetime.now()
        event_date = (current_time + timedelta(days=days_shift)).replace(hour=0, minute=0, second=0,
                                                                         microsecond=0)  # format:
        after_event_date = (event_date + timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                    microsecond=0)  # .strftime("%Y-%m-%d %H:%M:%S")

        try:
            # now = datetime.utcnow()
            stmt = select(Event).options(selectinload(Event.visitor)).order_by(Event.id).filter(and_(
                Event.date_time > event_date, Event.date_time < after_event_date
            ))
            result: Result = await session.execute(stmt)
            events = result.scalars().all()
            return events
        except Exception as e:
            print(e)


async def get_users_for_event(event):
    print("get_users_for_event")
    users_list = []
    async with db_helper.async_session_factory() as session:
        for visitor in event.visitor:
            try:
                user = await session.get(User, visitor.visitor_id)
                users_list.append(user)
            except Exception as e:
                print(f"Error: {e}")
    return users_list


async def send_mail_by_event(event):
    print(f"send_mail_by_event(event)")

    current_time = datetime.now()

    token = ACCESS_MESSAGE_GROUP_TOKEN
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    message = f"Название - {event.name}\nДата - {event.date_time}\nВремя - {event.time_start}"
    message = f"{message}\nВремя отправления - {current_time}"

    users = await get_users_for_event(event)

    for user in users:
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


async def send_mail_by_events(events):
    print(f"send_mail_by_events(events)")

    current_time = datetime.now()

    token = ACCESS_MESSAGE_GROUP_TOKEN
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    for event in events:

        message = f"Название - {event.name}\nДата - {event.date_time}\nВремя - {event.time_start}"
        message = f"{message}\nВремя отправления - {current_time}"

        users = await get_users_for_event(event)

        for user in users:
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


async def mail_task_any_days_before(days_shift):
    print("mail_task_any_days_before")
    events = await get_events_by_date(days_shift)
    await send_mail_by_events(events)


async def mail_task_any_hours_minutes_before(event):
    print("mail_task_any_hours_minutes_before")
    await send_mail_by_event(event)


# функция - задание
async def make_periodical_tasks():
    current_time = datetime.now()
    # task_execute_date = (current_time + timedelta(days=days_shift)).replace(hour=0, minute=0, second=0,
    #                                                                         microsecond=0)

    # Ставим задачи по авторассылкам по мероприятиям из БД
    print("Получаем задачи из БД из бд")
    async with db_helper.async_session_factory() as session:
        auto_event_mails = await crud.get_auto_event_mails(session=session)

        for mail_task_id, auto_event_mail in enumerate(auto_event_mails):

            # Выставление стандартного времени
            task_execute_date = (current_time + timedelta(minutes=1))

            # Если указан сдвиг по дню days_shift, то выставляем рсасылку на стандартное время,
            # которые будут, через указанное кол-ов дней, БЕЗ УЧЁТА ДРУГИХ СДВИГОВ
            if auto_event_mail.days_shift is not None and auto_event_mail.days_shift != 0:
                global_scheduler.add_job(
                    mail_task_any_days_before,
                    args=[auto_event_mail.days_shift], trigger='date',
                    run_date=task_execute_date.strftime("%Y-%m-%d %H:%M:%S"),
                    misfire_grace_time=60,  # sec
                )
                global_scheduler.print_jobs()
            # Если кол-во дней НЕ указано - проверяем все мероприятия на текущий день
            # Выставляем время рассылки по сдвигам hours_shift, minutes_shift
            else:
                # Постановка задач для рассылки для каждого мероприятия за определённое время до начала
                events_today = await get_events_by_date(0)

                for event_id, event in enumerate(events_today):
                    time_start = event.time_start
                    hour_start, min_start = tuple(time_start.split(":"))

                    event_start_datetime = datetime(
                        current_time.year,
                        current_time.month,
                        current_time.day,
                        int(hour_start),
                        int(min_start)
                    )

                    task_execute_date = (event_start_datetime - timedelta(
                        hours=int(auto_event_mail.hours_shift or 0),
                        minutes=int(auto_event_mail.minutes_shift or 0)
                    ))

                    job_id = f"mail_task_any_hours_minutes_before_{mail_task_id}{event_id}_{event.name}"
                    global_scheduler.add_job(
                        mail_task_any_hours_minutes_before,
                        args=[event], trigger='date',
                        run_date=task_execute_date.strftime("%Y-%m-%d %H:%M:%S"),
                        misfire_grace_time=300,
                        replace_existing=True,
                        id=job_id
                    )
                global_scheduler.print_jobs()

