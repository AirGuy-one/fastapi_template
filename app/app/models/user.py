import enum

from flask_login import UserMixin
from sqlalchemy import Column, Enum

from app.models.mixins.base import UUIDMixin, TimestampedMixin, SerializerMixin
from app.models.mixins.user import AbstractUser
from app.db.base import Base


class UserRole(enum.Enum):
    super_user = "Администратор"
    user = "Пользователь"


class User(AbstractUser, SerializerMixin, UUIDMixin, TimestampedMixin, UserMixin, Base):
    """Модель пользователя"""

    role = Column(Enum(UserRole), doc="Роль пользователя", default=UserRole.user)

    __tablename__ = 'user'

    def __repr__(self) -> str:
        return f"Пользователь: {self.id} | {self.login}"
