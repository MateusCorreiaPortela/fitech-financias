from decimal import Decimal
from pydantic import BaseModel


class SummaryResponse(BaseModel):
    month: str
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    transaction_count: int
