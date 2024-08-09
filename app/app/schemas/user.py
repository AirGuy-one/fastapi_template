from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.user import UserRole


class UserSchema(BaseModel):
    id: UUID | None = Field(title="ID", default=None)
    login: str = Field(title="Логин")
    is_active: bool = Field(title="Активность")
    created_at: datetime = Field(title="Создан", default_factory=datetime.now)
    updated_at: datetime = Field(title="Обновлен", default_factory=datetime.now)
    role: UserRole = Field(title="Роль пользователя", default=UserRole.user)
