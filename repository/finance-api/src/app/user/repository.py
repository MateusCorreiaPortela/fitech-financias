from src.app.core.base_repository import BaseRepository
from src.app.core.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
