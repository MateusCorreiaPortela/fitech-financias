from datetime import date
from decimal import Decimal
from tortoise.functions import Sum, Coalesce
from src.app.core.base_repository import BaseRepository
from src.app.core.models import Transaction


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    async def _get_totals(self, qs) -> dict[str, Decimal]:
        zero = Decimal("0.00")
        result = await (
            qs.annotate(
                total_income=Coalesce(Sum("amount", _filter={"type": "income"}), zero),
                total_expense=Coalesce(Sum("amount", _filter={"type": "expense"}), zero),
            ).values("total_income", "total_expense")
        )
        if not result:
            return {"total_income": zero, "total_expense": zero}
        return result[0]

    async def get_totals_by_user(self, user_id: int) -> dict[str, Decimal]:
        return await self._get_totals(self.model.filter(user_id=user_id))

    async def get_totals_by_user_and_period(self, user_id: int, date_from: date, date_to: date) -> dict[str, Decimal]:
        return await self._get_totals(self.model.filter(user_id=user_id, date__gte=date_from, date__lte=date_to))

    async def get_expense_by_category(self, user_id: int) -> list[dict]:
        return await (
            self.model.filter(user_id=user_id, type="expense")
            .annotate(total=Sum("amount"))
            .group_by("category_id", "category__name")
            .values("category_id", category_name="category__name", total="total")
        )

    async def get_income_vs_expense_by_month(self, user_id: int) -> list[dict]:
        rows = await self.model.raw(
            "SELECT DATE_FORMAT(date, '%%Y-%%m') as month, type, SUM(amount) as total "
            "FROM transactions WHERE user_id=%s GROUP BY month, type ORDER BY month",
            [user_id],
        )
        return [{"month": r.month, "type": r.type, "total": r.total} for r in rows]
