from fastapi import APIRouter

from app.core.user_manager import fastapi_users_obj
from app.schemas.user import UserOAuthRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users_obj.get_users_router(UserOAuthRead, UserUpdate),
)
