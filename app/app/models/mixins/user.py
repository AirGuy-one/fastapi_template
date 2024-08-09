from sqlalchemy import Column, String, Boolean


class AbstractUser:
    """Базовая модель пользователя"""

    login = Column(String(255), doc="Логин")
    password = Column(String(80), doc="Пароль")
    is_active = Column(Boolean, default=True, doc="Активность")
