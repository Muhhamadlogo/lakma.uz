from sqlalchemy.orm import Session

from app.models import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def ensure_by_telegram(self, telegram_id: int) -> User:
        user = self.repo.get_by_telegram_id(telegram_id)
        if user:
            return user
        return self.repo.create_telegram_user(telegram_id)
