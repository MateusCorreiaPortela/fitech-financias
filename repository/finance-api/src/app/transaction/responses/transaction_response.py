from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    description: str
    type: str
    date: date
    category_id: int
    category_name: str = ""
    created_at: datetime

    class Config:
        from_attributes = True
