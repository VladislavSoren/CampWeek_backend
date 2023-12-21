import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware as CORSMiddleware

from api_v1 import router as router_v1
from api_v1.mail.auto_event_mail import make_tasks
from core.config import settings



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

scheduler = AsyncIOScheduler()


# https://ahaw021.medium.com/scheduled-jobs-with-fastapi-and-apscheduler-5a4c50580b0e
@app.on_event("startup")
async def load_schedule_or_create_blank():
    global scheduler
    try:
        days_shift = 2

        # jobstores = {
        # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        # }
        # Schedule = AsyncIOScheduler(jobstores=jobstores)
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            make_tasks, args=[scheduler, days_shift], id='trigger_task', trigger='cron', minute='*/3')
        scheduler.start()
    except Exception as e:
        print(e)


@app.get("/")
def index():
    return {"Ping to the service root was successful!"}


if __name__ == "__main__":
    # # run app on the host and port
    uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=True)
    # uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=False, log_level="debug",
    #             workers=1, limit_concurrency=1, limit_max_requests=1)
