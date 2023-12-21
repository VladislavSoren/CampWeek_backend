from datetime import datetime, timedelta

import vk_api
from sqlalchemy import select, Result, and_
from sqlalchemy.orm import selectinload

from core.config import ACCESS_MESSAGE_GROUP_TOKEN
from core.models import db_helper, Event, User


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


async def send_mail(events):
    print(f"Рассылка по мероприятию")

    current_time = datetime.now()

    token = ACCESS_MESSAGE_GROUP_TOKEN
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    for event in events:
        users = await get_users_for_event(event)

        for user in users:
            user_id = user.vk_id

            random_id = 0
            try:
                response = vk.messages.send(
                    user_id=user_id,
                    random_id=random_id,
                    message=f"Ping_{current_time}",
                )
            except vk_api.exceptions.ApiError as e:
                print(e)


async def mail_task(days_shift):
    print("mail_task")
    events = await get_events_by_date(days_shift)
    await send_mail(events)


# функция - задание
async def make_tasks(scheduler, days_shift):
    # Get events that will start in 2 days
    current_time = datetime.now()
    task_execute_date = (current_time + timedelta(minutes=1))
    # task_execute_date = (current_time + timedelta(days=days_shift)).replace(hour=0, minute=0, second=0,
    #                                                                         microsecond=0)

    print("Создание задач по данным из бд")
    # планирование задания
    scheduler.add_job(
        mail_task,
        args=[days_shift], trigger='date',
        run_date=task_execute_date.strftime("%Y-%m-%d %H:%M:%S"))
    scheduler.print_jobs()
