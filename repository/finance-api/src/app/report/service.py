from src.app.transaction.service import TransactionService
from src.app.transaction.repository import TransactionRepository


class ReportService:
    def __init__(self):
        self.repository = TransactionRepository()
        self.transaction_service = TransactionService()

    async def summary(self, user_id: int) -> dict:
        return await self.transaction_service.get_summary(user_id)

    async def expense_by_category(self, user_id: int) -> list[dict]:
        return await self.repository.get_expense_by_category(user_id)

    async def income_vs_expense(self, user_id: int) -> list[dict]:
        return await self.repository.get_income_vs_expense_by_month(user_id)
