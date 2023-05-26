import re
import uuid
from typing import AsyncGenerator, Optional

from fastapi import Depends, Request
from fastapi_mail import MessageSchema, MessageType
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
    UUIDIDMixin,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from httpx_oauth.clients.google import GoogleOAuth2
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.mail_service import fm
from app.core.job_queue import q
from app.db.session import async_session
from app.models.user import OAuthAccount, User
from app.schemas import UserCreate

GOOGLE_PROFILE_ENDPOINT = "https://people.googleapis.com/v1/people/me"
google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_OAUTH_CLIENT_ID, settings.GOOGLE_OAUTH_CLIENT_SECRET
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def validate_password(self, password: str, user: UserCreate | User):
        regex = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{6,}$"
        is_password_strong = bool(re.match(regex, password))
        if not is_password_strong:
            raise InvalidPasswordException("Weak password")
        if user.email in password:
            raise InvalidPasswordException("Password should not contain email")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(  # type: ignore
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        reset_password_url = settings.FRONTEND_RESET_PASSWORD_PAGE + "?token=" + token
        message = MessageSchema(
            subject="Reset password request",
            recipients=[user.email],
            body=f"""You requested to reset password. Click the link below to change your password: {reset_password_url}""",
            subtype=MessageType.plain,
        )
        q.enqueue(fm.send_message, message)
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users_obj = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users_obj.current_user(active=True)
