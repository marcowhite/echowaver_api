from pydantic import BaseModel
from typing import Optional
from fastapi_users import schemas


class SUserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    display_name: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserUpdate(schemas.BaseUserUpdate):
    pass


class SUser(SUserCreate):
    id: int

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    is_public: bool = True

    role: int = 0

    city: Optional[str]
    bio: Optional[str]

    url: Optional[str]
    avatar: Optional[str]
    background: Optional[str]
    spotlight: Optional[str]

class SUserRead(schemas.BaseUser[int]):
    id: int

    email: str
    display_name: str
    first_name: Optional[str]
    last_name: Optional[str]

    is_active: bool
    is_superuser: bool
    is_verified: bool
    is_public: bool

    role: int = 0

    city: Optional[str]
    bio: Optional[str]

    url: Optional[str]
    avatar: Optional[str]
    background: Optional[str]
    spotlight: Optional[str]
