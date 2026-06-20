from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RouteBase(BaseModel):
    pass


class RouteCreate(RouteBase):
    pass


class RouteUpdate(RouteBase):
    pass


class RouteOut(RouteBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
