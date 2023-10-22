import datetime

import requests
from fastapi import APIRouter, Depends, Request, status, Response

# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from api_v1.user import crud
from api_v1.user.dependencies import user_by_id
from api_v1.user.schemas import User, UserCreate
from api_v1.user.utils import create_access_token, create_refresh_token
from core.config import settings
from core.models import db_helper

# router
router = APIRouter(
    tags=["User"],
)


@router.get("/vk_auth_start/", status_code=status.HTTP_200_OK)
async def vk_auth_start(request: Request):
    callback_url = str(request.url).replace("vk_auth_start", "vk_auth_callback")
    vk_auth_url = settings.vk_auth_url + f"&redirect_uri={callback_url}"
    return RedirectResponse(vk_auth_url)


@router.get("/vk_auth_callback/", response_class=RedirectResponse)
async def vk_auth_callback(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    code_str = request.query_params  # 'code=77988c5befef82f190'

    if not code_str:
        return {"message": "Code not provided"}

    # получаем токен доступа
    redirect_uri_with_code = str(request.url).replace("?code", "&code")
    access_token_url = settings.access_token_url + f"&redirect_uri={redirect_uri_with_code}"
    response_token = requests.get(access_token_url)
    access_token_data = response_token.json()

    if "access_token" not in access_token_data:
        return {"message": "Access token not provided"}

    # делаем запрос для получания данных юзера
    fields = "&fields=sex,city,bdate"
    user_info_url = settings.user_info_request_url + f"&access_token={access_token_data['access_token']}{fields}"
    user_info_response = requests.get(user_info_url)
    user_info_data = user_info_response.json()

    if "response" not in user_info_data:
        return {"message": "User data not available"}

    vk_user_info = user_info_data["response"][0]

    date_string = vk_user_info.get("bdate")
    parsed_date = datetime.datetime.strptime(date_string, "%d.%m.%Y")

    user = UserCreate(
        vk_id=vk_user_info["id"],
        first_name=vk_user_info["first_name"],
        last_name=vk_user_info["last_name"],
        sex=vk_user_info.get("sex"),
        city=vk_user_info.get("city")["title"],
        bdate=parsed_date,
    )

    # creating user
    _ = await crud.create_user(session=session, user_in=user)

    # get created user
    created_user = await crud.get_user_by_vk_id(session=session, user_vk_id=vk_user_info["id"])

    # set redirect response
    response = RedirectResponse(url=settings.ACCOUNT_PAGE_URL, status_code=status.HTTP_303_SEE_OTHER)

    # add cookie in response
    response.set_cookie(key="access_token", value=create_access_token(created_user.id))
    response.set_cookie(key="refresh_token", value=create_refresh_token(created_user.id))

    return response


# work!
@router.get("/cookieset", response_class=RedirectResponse)
def cookie_set2() -> RedirectResponse:
    token = "fake_token"
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="token", value=token)
    return response


@router.get("/", response_model=list[User])
async def get_users(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.get("/{user_id}/", response_model=User)
async def get_user(
    user: User = Depends(user_by_id),
    # token: str = Depends(oauth2_scheme)
):
    # token
    return user


# @router.get("/{auto_id}/drivers/", response_model=list[Driver])
# async def get_all_auto_drivers(
#     auto_id: int,
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
#     _: Auto = Depends(auto_by_id),  # check if user is exist
# ):
#     return await crud.get_all_auto_drivers(session, auto_id)
#
#
# @router.get("/{auto_id}/routes/", response_model=list[Route])
# async def get_all_auto_routes(
#     auto_id: int,
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
#     _: Auto = Depends(auto_by_id),  # check if user is exist
# ):
#     return await crud.get_all_auto_routes(session, auto_id)
