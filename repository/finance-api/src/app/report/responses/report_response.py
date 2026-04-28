from decimal import Decimal
from pydantic import BaseModel


class ExpenseByCategoryItem(BaseModel):
    category_id: int
    category_name: str
    total: Decimal


class IncomeVsExpenseItem(BaseModel):
    month: str
    type: str
    total: Decimal
