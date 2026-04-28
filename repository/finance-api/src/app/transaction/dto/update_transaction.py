from datetime import date as dt
from decimal import Decimal
from pydantic import BaseModel, field_validator
from src.app.transaction.dto.create_transaction import TransactionType


class UpdateTransactionDto(BaseModel):
    amount: Decimal | None = None
    description: str | None = None
    category_id: int | None = None
    date: dt | None = None
    type: TransactionType | None = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v <= 0:
            raise ValueError("Amount must be positive")
        return v
