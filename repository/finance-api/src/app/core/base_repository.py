from typing import TypeVar, Generic, Type, Optional
from tortoise import Model
from tortoise.queryset import QuerySet

T = TypeVar("T", bound=Model)


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    def query(self) -> QuerySet[T]:
        return self.model.all()

    async def find_one(self, **where) -> Optional[T]:
        return await self.model.filter(**where).first()

    async def find_one_by_id(self, id: int) -> Optional[T]:
        return await self.model.filter(id=id).first()

    async def find_many(self, **where) -> list[T]:
        return await self.model.filter(**where)

    async def find_all(self) -> list[T]:
        return await self.model.all()

    async def create(self, **data) -> T:
        return await self.model.create(**data)

    async def update_by_id(self, id: int, **data) -> Optional[T]:
        instance = await self.find_one_by_id(id)
        if not instance:
            return None
        await instance.update_from_dict(data).save()
        return instance

    async def delete_by_id(self, id: int) -> bool:
        deleted = await self.model.filter(id=id).delete()
        return deleted > 0

    async def count(self, **where) -> int:
        return await self.model.filter(**where).count()

    async def exists(self, **where) -> bool:
        return await self.model.filter(**where).exists()
