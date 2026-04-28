from datetime import date
from decimal import Decimal
from tortoise import connections
from src.app.core.base_repository import BaseRepository
from src.app.core.models import Transaction

ZERO = Decimal("0.00")


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    async def _get_totals(self, user_id: int, date_from: date | None = None, date_to: date | None = None) -> dict[str, Decimal]:
        conn = connections.get("default")
        sql = "SELECT type, COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id=%s"
        params: list = [user_id]
        if date_from:
            sql += " AND date >= %s"
            params.append(date_from)
        if date_to:
            sql += " AND date <= %s"
            params.append(date_to)
        sql += " GROUP BY type"
        _, rows = await conn.execute_query(sql, params)
        result = {"total_income": ZERO, "total_expense": ZERO}
        for row in rows:
            if row["type"] == "income":
                result["total_income"] = Decimal(str(row["total"]))
            elif row["type"] == "expense":
                result["total_expense"] = Decimal(str(row["total"]))
        return result

    async def get_totals_by_user(self, user_id: int) -> dict[str, Decimal]:
        return await self._get_totals(user_id)

    async def get_totals_by_user_and_period(self, user_id: int, date_from: date, date_to: date) -> dict[str, Decimal]:
        return await self._get_totals(user_id, date_from, date_to)

    async def get_expense_by_category(self, user_id: int) -> list[dict]:
        conn = connections.get("default")
        sql = (
            "SELECT t.category_id, c.name as category_name, SUM(t.amount) as total "
            "FROM transactions t JOIN categories c ON t.category_id = c.id "
            "WHERE t.user_id=%s AND t.type='expense' "
            "GROUP BY t.category_id, c.name"
        )
        _, rows = await conn.execute_query(sql, [user_id])
        return [
            {"category_id": r["category_id"], "category_name": r["category_name"], "total": Decimal(str(r["total"]))}
            for r in rows
        ]

    async def get_income_vs_expense_by_month(self, user_id: int) -> list[dict]:
        conn = connections.get("default")
        sql = (
            "SELECT DATE_FORMAT(date, '%%Y-%%m') as month, type, SUM(amount) as total "
            "FROM transactions WHERE user_id=%s "
            "GROUP BY month, type ORDER BY month"
        )
        _, rows = await conn.execute_query(sql, [user_id])
        return [
            {"month": r["month"], "type": r["type"], "total": Decimal(str(r["total"]))}
            for r in rows
        ]
