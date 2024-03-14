from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.mail import crud
from api_v1.mail.crud import make_manual_mailing
from api_v1.mail.dependencies import auto_event_mail_by_id
from api_v1.mail.schemas import (
    AutoEventMail,
    AutoEventMailCreate,
    AutoEventMailUpdatePartial,
)
from core.models import db_helper

# router
router = APIRouter(
    tags=["AutoEventMail"],
)


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_auto_event_mail(
    auto_event_mail_in: AutoEventMailCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    response = await crud.create_auto_event_mail(session=session, auto_event_mail_in=auto_event_mail_in)
    return f"Response status: {response}"


@router.get("/", response_model=list[AutoEventMail])
async def get_auto_event_mails(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_auto_event_mails(session=session)


@router.get("/all/", response_model=list[AutoEventMail])
async def get_all_auto_event_mails(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_auto_event_mails(session=session)


@router.get("/{auto_event_mail_id}/", response_model=AutoEventMail)
async def get_auto_event_mail(
    auto_event_mail: AutoEventMail = Depends(auto_event_mail_by_id),
    # token: str = Depends(oauth2_scheme)
):
    # token
    return auto_event_mail


@router.patch("/{auto_event_mail_id}/", response_model=AutoEventMail)
async def update_auto_event_mail_partial(
    auto_event_mail_update: AutoEventMailUpdatePartial,
    auto_event_mail: AutoEventMail = Depends(auto_event_mail_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_auto_event_mail(
        auto_event_mail_update=auto_event_mail_update,
        auto_event_mail=auto_event_mail,
        session=session,
        partial=True,
    )


@router.patch("/{auto_event_mail_id}/restore/", response_model=AutoEventMail)
async def auto_event_mail_restore(
    auto_event_mail_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.restore_auto_event_mail(
        auto_event_mail_id=auto_event_mail_id,
        session=session,
    )

    return await auto_event_mail_by_id(auto_event_mail_id, session)


@router.delete("/{auto_event_mail_id}/delete/", response_model=AutoEventMail)
async def auto_event_mail_archive(
    auto_event_mail_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.archive_auto_event_mail(
        auto_event_mail_id=auto_event_mail_id,
        session=session,
    )

    return await auto_event_mail_by_id(auto_event_mail_id, session)


@router.post("create_manual_mail_task_by_users/", status_code=status.HTTP_201_CREATED)
async def create_manual_mail_task_by_users(
    any_registered: bool,
    auto_event_mail_update: AutoEventMailUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await make_manual_mailing(
        session=session,
        event_mail_task=auto_event_mail_update,
        any_registered=any_registered,
    )
    return "Mailed"
