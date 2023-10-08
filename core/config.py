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

    # for form auth URL
    SOCIAL_AUTH_VK_OAUTH2_KEY: str = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY")
    SOCIAL_AUTH_VK_OAUTH2_SECRET: str = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET")
    VK_API_VERSION: str = os.getenv("VK_API_VERSION")

    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    DB_ECHO: bool = True

    db_echo: bool = True

    vk_auth_url: str = f"https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&response_type=code&display=page&v={VK_API_VERSION}"
    access_token_url: str = f"https://oauth.vk.com/access_token?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&client_secret={SOCIAL_AUTH_VK_OAUTH2_SECRET}&response_type=code&v={VK_API_VERSION}"
    user_info_request_url: str = f"https://api.vk.com/method/users.get?v={VK_API_VERSION}"

    # router prefixes
    user_prefix: str = "/user"


settings = Setting()
