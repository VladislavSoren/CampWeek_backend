import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DB_PORT_OUT = os.getenv("DB_PORT_OUT")


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    DB_ECHO: bool = True

    db_echo: bool = True


settings = Setting()
