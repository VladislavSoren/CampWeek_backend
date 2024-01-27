from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.params import Path

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.role import crud
from api_v1.role.dependencies import role_by_id
from api_v1.role.schemas import Role, RoleCreate, RoleUpdatePartial
from core.models import db_helper

# router
router = APIRouter(
    tags=["Role"],
)


@router.post("/", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_role(session=session, role_in=role_in)


@router.get("/", response_model=list[Role])
async def get_roles(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_roles(session=session)


@router.get("/all/", response_model=list[Role])
async def get_all_roles(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_roles(session=session)


@router.get("/{role_id}/", response_model=Role)
async def get_role(
    role: Role = Depends(role_by_id),
    # token: str = Depends(oauth2_scheme)
):
    # token
    return role


@router.patch("/{role_id}/", response_model=Role)
async def update_role_partial(
    role_update: RoleUpdatePartial,
    role: Role = Depends(role_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_role(
        role_update=role_update,
        role=role,
        session=session,
        partial=True,
    )


@router.patch("/{role_id}/restore/", response_model=Role)
async def archive_role(
    role_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.restore_role(
        role_id=role_id,
        session=session,
    )

    return await role_by_id(role_id, session)


@router.delete("/{role_id}/", response_model=Role)
async def archive_role(
    role_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.archive_role(
        role_id=role_id,
        session=session,
    )

    return await role_by_id(role_id, session)
