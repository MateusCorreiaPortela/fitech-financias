import math
from fastapi import HTTPException
from src.app.category.dto import CreateCategoryDto, UpdateCategoryDto
from src.app.category.repository import CategoryRepository
from src.app.core.models import Category


class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    async def create(self, user_id: int, dto: CreateCategoryDto) -> Category:
        if await self.repository.exists(name=dto.name, user_id=user_id):
            raise HTTPException(status_code=409, detail="Category already exists")
        return await self.repository.create(name=dto.name, user_id=user_id)

    async def find_all_by_user(self, user_id: int, page: int, limit: int) -> dict:
        qs = self.repository.model.filter(user_id=user_id)
        total = await qs.count()
        offset = (page - 1) * limit
        items = await qs.offset(offset).limit(limit)
        return {
            "items": items,
            "total": total,
            "page": page,
            "pages": math.ceil(total / limit) if total else 1,
            "limit": limit,
        }

    async def find_by_id(self, id: int, user_id: int) -> Category:
        category = await self.repository.find_one(id=id, user_id=user_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def update(self, id: int, user_id: int, dto: UpdateCategoryDto) -> Category:
        category = await self.find_by_id(id, user_id)
        await category.update_from_dict(dto.model_dump()).save()
        return category

    async def delete(self, id: int, user_id: int) -> None:
        await self.find_by_id(id, user_id)
        await self.repository.model.filter(id=id, user_id=user_id).delete()
