
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal
from datetime import datetime


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# USER SCHEMAS
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(pattern=r"^[0-9]{10,15}$")
    password: str = Field(min_length=8, max_length=128)
    status: Literal["active", "inactive"] = "active"


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^[0-9]{10,15}$")
    status: Literal["active", "inactive"] | None = None


class UserResponse(BaseSchema):
    id: int
    name: str
    email: EmailStr
    phone: str
    role: Literal["teacher", "student"]
    status: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# TASK SCHEMAS
class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = None
    status: Literal["pending", "in progress", "done"] = "pending"
    user_id: int = Field(gt=0)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    work_notes: str | None = None
    status: Literal["pending", "in progress", "done"] | None = None
    user_id: int | None = Field(default=None, gt=0)


class TaskResponse(BaseSchema):
    id: int
    title: str
    description: str | None
    work_notes: str | None
    status: str
    user_id: int
    created_at: datetime


class UserWithTasks(UserResponse):
    tasks: list[TaskResponse] = Field(default_factory=list)