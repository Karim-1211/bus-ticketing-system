from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BusBase(BaseModel):
    pass


class BusCreate(BusBase):
    pass


class BusUpdate(BusBase):
    pass


class BusOut(BusBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
