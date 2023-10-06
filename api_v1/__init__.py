from fastapi import APIRouter

from .event.views import router as driver_router
from .user.views import router as auto_router

router = APIRouter()
router.include_router(router=auto_router, prefix="/user")
router.include_router(router=driver_router, prefix="/event")
