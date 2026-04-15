from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        return self.db.scalars(stmt).first()

    def create_telegram_user(self, telegram_id: int) -> User:
        user = User(telegram_id=telegram_id, username=f"tg_{telegram_id}", first_name="Telegram", last_name="User")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
