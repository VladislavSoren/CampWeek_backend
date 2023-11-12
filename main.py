import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware as CORSMiddleware

from api_v1 import router as router_v1
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


@app.get("/")
def index():
    return {"Ping to the service root was successful!"}


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run("main:app", host="0.0.0.0", port=5777, reload=True)
