import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings

app = FastAPI()
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def index():
    return {"Ping to the service root was successful!"}


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
