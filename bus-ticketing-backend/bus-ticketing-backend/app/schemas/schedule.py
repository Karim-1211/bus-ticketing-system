from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScheduleBase(BaseModel):
    pass


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(ScheduleBase):
    pass


class ScheduleOut(ScheduleBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
