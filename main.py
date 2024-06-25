from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Result, select

from api_v1 import router as router_v1
from api_v1.groupvk.schemas import GroupVKCreate
from api_v1.mail.auto_event_mail import make_periodical_tasks
from core.config import GROUP_TOKEN_DICT, settings
from core.crypto import encrypt_message, generate_key, load_key
from core.models import GroupVK, db_helper
from init_global_shedular import global_scheduler

# from starlette.middleware.cors import CORSMiddleware as CORSMiddleware


app = FastAPI()

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

origins = settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# https://ahaw021.medium.com/scheduled-jobs-with-fastapi-and-apscheduler-5a4c50580b0e
@app.on_event("startup")
async def load_schedule_or_create_blank():
    # Генерируем секретный ключ
    generate_key()
    key = load_key()

    # Наполняем таблицу GroupVK зашифрованных токенами
    async with db_helper.async_session_factory() as session:
        stmt = select(GroupVK.name)
        result: Result = await session.execute(stmt)
        groups_bd = result.scalars().all()

        for name, token in GROUP_TOKEN_DICT.items():
            if name not in set(groups_bd):
                new_obj = GroupVKCreate(name=name, token=encrypt_message(token, key).decode())

                user = GroupVK(**new_obj.model_dump())
                session.add(user)

        await session.commit()

    current_time = datetime.now()
    task_execute_date = current_time + timedelta(minutes=1)

    try:
        global_scheduler.add_job(
            make_periodical_tasks,
            id="trigger_task",
            trigger="cron",
            minute="*/1",
            start_date=task_execute_date.strftime("%Y-%m-%d %H:%M:%S"),
            misfire_grace_time=60,
        )

        print(f"scheduler main.py id - {id(global_scheduler)}")
        global_scheduler.start()  # Necessarily to add periodical task before scheduler start!
        global_scheduler.print_jobs()

    except Exception as e:
        print(e)


@app.on_event("shutdown")
async def shutdown_event():
    global_scheduler.print_jobs()
    global_scheduler.shutdown()


@app.get("/")
def index():
    return "Ping to the service root was successful!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=False, log_level="debug")
