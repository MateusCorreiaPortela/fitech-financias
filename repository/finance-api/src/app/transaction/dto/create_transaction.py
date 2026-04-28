from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class CreateTransactionDto(BaseModel):
    amount: float
    description: str
    category_id: int
    date: date
    type: TransactionType

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v
