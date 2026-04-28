from src.app.core.base_repository import BaseRepository
from src.app.core.models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)
