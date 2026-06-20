from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
