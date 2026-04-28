from datetime import date
from src.app.transaction.dto.create_transaction import TransactionType


class TransactionFilterDto:
    def __init__(
        self,
        type: TransactionType | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        order_by: str = "-date",
    ):
        self.type = type
        self.date_from = date_from
        self.date_to = date_to
        self.order_by = order_by
