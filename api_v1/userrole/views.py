from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.userrole import crud
from api_v1.userrole.dependencies import userrole_by_id
from api_v1.userrole.schemas import UserRole, UserRoleUpdatePartial, UserRoleCreate
from core.models import db_helper

# router
router = APIRouter(
    tags=["UserRole"],
)


@router.post("/", response_model=UserRole, status_code=status.HTTP_201_CREATED)
async def create_userrole(
        userrole_in: UserRoleCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_userrole(session=session, userrole_in=userrole_in)


@router.get("/", response_model=list[UserRole])
async def get_userrole(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_userroles(session=session)


@router.get("/{obj_id}/", response_model=UserRole)
async def get_userrole(
        userrole: UserRole = Depends(userrole_by_id),
        # token: str = Depends(oauth2_scheme)
):
    # token
    return userrole


@router.patch("/{obj_id}/", response_model=UserRole)
async def update_userrole_partial(
        userrole_update: UserRoleUpdatePartial,
        userrole: UserRole = Depends(userrole_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_userrole(
        userrole_update=userrole_update,
        userrole=userrole,
        session=session,
        partial=True,
    )
