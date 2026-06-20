from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookingBase(BaseModel):
    pass


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
