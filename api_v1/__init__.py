from fastapi import APIRouter

from core.config import settings

# from .event.views import router as driver_router
from .user.views import router as auto_router

router = APIRouter()
router.include_router(router=auto_router, prefix=settings.user_prefix)
# router.include_router(router=driver_router, prefix="/event")
