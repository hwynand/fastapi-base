import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserOAuthRead(UserRead, schemas.BaseOAuthAccountMixin):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str
