from fastapi import APIRouter, Depends, Request, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.role.schemas import Role
from api_v1.user.schemas import User
from api_v1.userrole import crud
from api_v1.role.crud import get_role_by_name
from api_v1.userrole.dependencies import userrole_by_id, has_role
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
async def get_userroles(
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


@router.get("/roles_of_user/{user_id}", response_model=list[Role])
async def get_roles_of_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_roles_of_user(session=session, user_id=user_id)


@router.get("/users_of_role/{role_id}", response_model=list[User])
async def get_users_of_role(
    role_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users_of_role(session=session, role_id=role_id)


@router.post("/give_admin_role/{user_id}", response_model=UserRole)
@has_role("superadmin")
async def give_admin_role(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    admin_role = await get_role_by_name(session, "admin")

    existing_roles = await crud.get_roles_of_user(session, user_id)
    user_role_names = {role.name for role in existing_roles}

    if not admin_role or not admin_role.name in user_role_names:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The 'admin' role not found or the user already has the 'admin' role.",
        )

    await crud.create_userrole(session, UserRoleCreate(user_id=user_id, role_id=admin_role.id))

    return await crud.get_roles_of_user(session, user_id=user_id)
