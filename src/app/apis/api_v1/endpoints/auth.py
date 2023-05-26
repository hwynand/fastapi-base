from fastapi import APIRouter

from app.core.config import settings
from app.core.user_manager import (
    auth_backend,
    fastapi_users_obj,
    google_oauth_client,
)
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

router.include_router(
    fastapi_users_obj.get_auth_router(auth_backend),
    prefix="/jwt",
)
router.include_router(
    fastapi_users_obj.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users_obj.get_reset_password_router(),
)
router.include_router(
    fastapi_users_obj.get_verify_router(UserRead),
)
router.include_router(
    fastapi_users_obj.get_oauth_router(
        google_oauth_client,
        auth_backend,
        settings.SECRET_KEY,
        str(settings.FRONTEND_HOME_PAGE),
    ),
    prefix="/google",
)
