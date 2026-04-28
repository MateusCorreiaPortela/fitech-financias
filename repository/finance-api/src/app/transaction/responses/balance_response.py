from decimal import Decimal
from pydantic import BaseModel


class BalanceResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
