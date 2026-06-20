from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    pass


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass


class NotificationOut(NotificationBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
