from pydantic import BaseModel, EmailStr
from typing import Optional, List
from fastapi_users import schemas


class SUserRoleAdd(BaseModel):
    name: str
    permissions: Optional[str] = None


class SUserRole(SUserRoleAdd):
    id: int


class SUserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    display_name: str


class SUserUpdate(schemas.BaseUserUpdate):
    email: EmailStr
    display_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_public: bool

    city: Optional[str]
    bio: Optional[str]

    url: Optional[str]
    avatar: Optional[str]
    background: Optional[str]
    spotlight: Optional[str]


class SUser(SUserCreate):
    id: int

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    is_public: bool = True

    first_name: Optional[str]
    last_name: Optional[str]

    role: int = 1

    city: Optional[str]
    bio: Optional[str]

    url: Optional[str]
    avatar: Optional[str]
    background: Optional[str]
    spotlight: Optional[str]


class SUserProfile(BaseModel):
    id: int

    display_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_public: bool

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

    role_id: int

    city: Optional[str]
    bio: Optional[str]

    url: Optional[str]
    avatar: Optional[str]
    background: Optional[str]
    spotlight: Optional[str]
