import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware as CORSMiddleware

from api_v1 import router as router_v1
from core.config import settings

from datetime import datetime, timedelta

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

import time
from apscheduler.schedulers.background import BackgroundScheduler


# # Создает ФОНОВЫЙ планировщик
# scheduler = BackgroundScheduler()

def send_mail(info):
    print(f"Рассылка по мероприятию {info}")


# функция - задание
def prompt():
    print("Запрос в БД")
    print("Создание задач по данным из бд")

    current_time = datetime.now()

    dates_list = [1, 2]
    for date_obj in dates_list:
        # планирование задания
        scheduler.add_job(
            send_mail,
            args=[date_obj], trigger='date',
            run_date=(current_time + timedelta(minutes=date_obj)).strftime("%Y-%m-%d %H:%M:%S"))

    scheduler.print_jobs()


# https://ahaw021.medium.com/scheduled-jobs-with-fastapi-and-apscheduler-5a4c50580b0e
@app.on_event("startup")
async def load_schedule_or_create_blank():
    global scheduler
    try:
        # jobstores = {
        # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        # }
        # Schedule = AsyncIOScheduler(jobstores=jobstores)
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            prompt, id='trigger_task', trigger='cron', minute='*/3')
        scheduler.start()
    except:
        pass


# scheduler.add_job(
#     prompt, id='trigger_task', trigger='cron', minute='*/3')
#
# # Запуск запланированных заданий
# scheduler.start()


@app.get("/")
def index():
    return {"Ping to the service root was successful!"}


if __name__ == "__main__":
    # # run app on the host and port
    # uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=True, workers=1)
    uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=False, log_level="debug",
                workers=1, limit_concurrency=1, limit_max_requests=1)
