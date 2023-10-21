import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

# db config variables
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DB_PORT_OUT = os.getenv("DB_PORT_OUT")

# auth via VK variables
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET")
SOCIAL_AUTH_VK_OAUTH2_KEY_PROD = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY_PROD")
SOCIAL_AUTH_VK_OAUTH2_SECRET_PROD = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET_PROD")
VK_API_VERSION = os.getenv("VK_API_VERSION")
FRONTEND_URL_LOCAL = os.getenv("FRONTEND_URL_LOCAL")
FRONTEND_URL_PROD = os.getenv("FRONTEND_URL_PROD")


class Config(BaseSettings):
    origins: list = [
        FRONTEND_URL_LOCAL,
        FRONTEND_URL_PROD,
        '109.201.65.62:5777',
        '127.0.0.1:5777',
        '127.0.0.1:3000',
        '109.201.65.62:5888',
    ]

    api_v1_prefix: str = "/api/v1"

    # for form auth URL
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    DB_ECHO: bool = True

    vk_auth_url: str = f"https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&response_type=code&display=page&v={VK_API_VERSION}"
    access_token_url: str = f"https://oauth.vk.com/access_token?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&client_secret={SOCIAL_AUTH_VK_OAUTH2_SECRET}&response_type=code&v={VK_API_VERSION}"
    user_info_request_url: str = f"https://api.vk.com/method/users.get?v={VK_API_VERSION}"

    # router prefixes
    user_prefix: str = "/user"


class DevelopmentConfigLocal(Config):
    pass


class DevelopmentConfigDocker(Config):
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@pg:{PORT}/{DB_NAME}"


class ProdConfig(Config):

    # for form auth URL
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@pg:{PORT}/{DB_NAME}"
    DB_ECHO: bool = True

    vk_auth_url: str = f"https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY_PROD}&response_type=code&display=page&v={VK_API_VERSION}"
    access_token_url: str = f"https://oauth.vk.com/access_token?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY_PROD}&client_secret={SOCIAL_AUTH_VK_OAUTH2_SECRET_PROD}&response_type=code&v={VK_API_VERSION}"
    user_info_request_url: str = f"https://api.vk.com/method/users.get?v={VK_API_VERSION}"


config_class_name = os.getenv("CONFIG_CLASS", "DevelopmentConfigLocal")
if config_class_name == "DevelopmentConfigDocker":
    CONFIG_OBJECT = DevelopmentConfigDocker
elif config_class_name == "ProdConfig":
    CONFIG_OBJECT = ProdConfig
else:
    CONFIG_OBJECT = DevelopmentConfigLocal

settings = CONFIG_OBJECT()
