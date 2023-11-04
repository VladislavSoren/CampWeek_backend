from fastapi import APIRouter

from core.config import settings

# from .event.views import router as driver_router
from .user.views import router as user_router
from .role.views import router as role_router
from .userrole.views import router as userrole

router = APIRouter()
router.include_router(router=user_router, prefix=settings.user_prefix)
router.include_router(router=role_router, prefix=settings.role_prefix)
router.include_router(router=userrole, prefix=settings.userrole_prefix)
# router.include_router(router=driver_router, prefix="/event")
