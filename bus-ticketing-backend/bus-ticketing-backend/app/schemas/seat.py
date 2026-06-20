from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SeatBase(BaseModel):
    pass


class SeatCreate(SeatBase):
    pass


class SeatUpdate(SeatBase):
    pass


class SeatOut(SeatBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
