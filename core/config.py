import os

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

# origins
FRONTEND_URL_LOCAL = os.getenv("FRONTEND_URL_LOCAL")
FRONTEND_URL_PROD = os.getenv("FRONTEND_URL_PROD")
BACKEND_URL_LOCAL = os.getenv("BACKEND_URL_LOCAL")
BACKEND_URL_PROD = os.getenv("BACKEND_URL_PROD")

# JWT
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
REFRESH_SECRET_KEY_JWT = os.getenv("REFRESH_SECRET_KEY_JWT")

# VK
GROUP_TOKEN_DICT = {
    "ACCESS_MESSAGE_GROUP_TOKEN_0": os.getenv("ACCESS_MESSAGE_GROUP_TOKEN_0"),
    "ACCESS_MESSAGE_GROUP_TOKEN_1": os.getenv("ACCESS_MESSAGE_GROUP_TOKEN_1"),
}


class Config(BaseSettings):
    origins: list = [
        FRONTEND_URL_LOCAL,
        FRONTEND_URL_PROD,
        BACKEND_URL_LOCAL,
        BACKEND_URL_PROD,
    ]

    api_v1_prefix: str = "/api/v1"

    # for form auth URL
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{DB_PORT_OUT}/{DB_NAME}"
    DB_ECHO: bool = False

    vk_auth_url: str = f"https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&response_type=code&display=page&v={VK_API_VERSION}"
    access_token_url: str = f"https://oauth.vk.com/access_token?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&client_secret={SOCIAL_AUTH_VK_OAUTH2_SECRET}&response_type=code&v={VK_API_VERSION}"
    user_info_request_url: str = f"https://api.vk.com/method/users.get?v={VK_API_VERSION}"

    # router prefixes
    user_prefix: str = "/user"
    role_prefix: str = "/role"
    userrole_prefix: str = "/userrole"
    event_prefix: str = "/event"
    eventspeaker_prefix: str = "/eventspeaker"
    eventvisitor_prefix: str = "/eventvisitor"
    mail_prefix: str = "/mail"
    region_prefix: str = "/region"

    # JWT
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30


class DevelopmentConfigLocal(Config):
    ACCOUNT_PAGE_URL: str = FRONTEND_URL_LOCAL + "/account"


class DevelopmentConfigDocker(Config):
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@pg:{PORT}/{DB_NAME}"
    ACCOUNT_PAGE_URL: str = FRONTEND_URL_LOCAL + "/account"


class ProdConfigLocal(Config):
    # for form auth URL
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{DB_PORT_OUT}/{DB_NAME}"

    vk_auth_url: str = f"https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY_PROD}&response_type=code&display=page&v={VK_API_VERSION}"
    access_token_url: str = f"https://oauth.vk.com/access_token?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY_PROD}&client_secret={SOCIAL_AUTH_VK_OAUTH2_SECRET_PROD}&response_type=code&v={VK_API_VERSION}"
    user_info_request_url: str = f"https://api.vk.com/method/users.get?v={VK_API_VERSION}"

    ACCOUNT_PAGE_URL: str = FRONTEND_URL_PROD + "/account"


class ProdConfigDocker(Config):
    # for form auth URL
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@pg:{PORT}/{DB_NAME}"

    vk_auth_url: str = f"https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY_PROD}&response_type=code&display=page&v={VK_API_VERSION}"
    access_token_url: str = f"https://oauth.vk.com/access_token?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY_PROD}&client_secret={SOCIAL_AUTH_VK_OAUTH2_SECRET_PROD}&response_type=code&v={VK_API_VERSION}"
    user_info_request_url: str = f"https://api.vk.com/method/users.get?v={VK_API_VERSION}"

    ACCOUNT_PAGE_URL: str = FRONTEND_URL_PROD + "/account"


config_class_name = os.getenv("CONFIG_CLASS", "DevelopmentConfigLocal")
if config_class_name == "DevelopmentConfigDocker":
    CONFIG_OBJECT = DevelopmentConfigDocker
elif config_class_name == "ProdConfigLocal":
    CONFIG_OBJECT = ProdConfigLocal
elif config_class_name == "ProdConfigDocker":
    CONFIG_OBJECT = ProdConfigDocker
else:
    CONFIG_OBJECT = DevelopmentConfigLocal

settings = CONFIG_OBJECT()
