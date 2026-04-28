import math
from datetime import date
from fastapi import HTTPException
from src.app.core.models import Transaction, Category
from src.app.transaction.dto import CreateTransactionDto, UpdateTransactionDto, TransactionFilterDto
from src.app.transaction.repository import TransactionRepository


class TransactionService:
    def __init__(self):
        self.repository = TransactionRepository()

    async def _validate_category(self, category_id: int, user_id: int) -> None:
        if not await Category.filter(id=category_id, user_id=user_id).exists():
            raise HTTPException(status_code=404, detail="Category not found")

    async def create(self, user_id: int, dto: CreateTransactionDto) -> dict:
        await self._validate_category(dto.category_id, user_id)
        tx = await self.repository.create(user_id=user_id, **dto.model_dump())
        await tx.fetch_related("category")
        return self._to_response(tx)

    async def find_all(self, user_id: int, filters: TransactionFilterDto, page: int, limit: int) -> dict:
        qs = self.repository.model.filter(user_id=user_id)
        if filters.type:
            qs = qs.filter(type=filters.type.value)
        if filters.date_from:
            qs = qs.filter(date__gte=filters.date_from)
        if filters.date_to:
            qs = qs.filter(date__lte=filters.date_to)

        total = await qs.count()
        offset = (page - 1) * limit
        items = await qs.order_by(filters.order_by).offset(offset).limit(limit).prefetch_related("category")

        return {
            "items": [self._to_response(tx) for tx in items],
            "total": total,
            "page": page,
            "pages": math.ceil(total / limit) if total else 1,
            "limit": limit,
        }

    async def find_by_id(self, id: int, user_id: int) -> dict:
        tx = await self.repository.model.filter(id=id, user_id=user_id).prefetch_related("category").first()
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return self._to_response(tx)

    async def update(self, id: int, user_id: int, dto: UpdateTransactionDto) -> dict:
        tx = await self.repository.model.filter(id=id, user_id=user_id).first()
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        data = dto.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=400, detail="No fields to update")
        if "category_id" in data:
            await self._validate_category(data["category_id"], user_id)
        await tx.update_from_dict(data).save()
        await tx.fetch_related("category")
        return self._to_response(tx)

    async def delete(self, id: int, user_id: int) -> None:
        if not await self.repository.model.filter(id=id, user_id=user_id).exists():
            raise HTTPException(status_code=404, detail="Transaction not found")
        await self.repository.model.filter(id=id, user_id=user_id).delete()

    async def get_balance(self, user_id: int) -> dict:
        totals = await self.repository.get_totals_by_user(user_id)
        return {
            "total_income": totals["total_income"],
            "total_expense": totals["total_expense"],
            "balance": totals["total_income"] - totals["total_expense"],
        }

    async def get_summary(self, user_id: int) -> dict:
        today = date.today()
        first_day = today.replace(day=1)
        totals = await self.repository.get_totals_by_user_and_period(user_id, first_day, today)
        count = await self.repository.model.filter(user_id=user_id, date__gte=first_day, date__lte=today).count()
        return {
            "month": today.strftime("%Y-%m"),
            "total_income": totals["total_income"],
            "total_expense": totals["total_expense"],
            "balance": totals["total_income"] - totals["total_expense"],
            "transaction_count": count,
        }

    @staticmethod
    def _to_response(tx: Transaction) -> dict:
        return {
            "id": tx.id,
            "amount": tx.amount,
            "description": tx.description,
            "type": tx.type,
            "date": tx.date,
            "category_id": tx.category_id,
            "category_name": tx.category.name if tx.category else "",
            "created_at": tx.created_at,
        }
