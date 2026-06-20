from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):
    pass


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class PaymentOut(PaymentBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
