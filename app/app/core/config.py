
import secrets

from enum import Enum

from pydantic import PostgresDsn, Field, computed_field, field_validator
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Settings(BaseSettings):
    """Настройки проекта"""

    api_v1_str: str = Field(title="Prefix для V1", default="/api/v1")
    debug: bool = Field(title="Режим отладки", default=True)
    secret_key: str = Field(title="Секретный ключ", default_factory=lambda: secrets.token_hex(16))
    log_level: LogLevel = Field(title="Уровень логирования", default=LogLevel.INFO)
    project_name: str = Field(title="Имя проекта", default="Unnamed", alias="PROJECT_SLUG")

    # region Настройки БД
    postgres_user: str = Field(title="Пользователь БД")
    postgres_password: str = Field(title="Пароль БД")
    postgres_host: str = Field(title="Хост БД")
    postgres_port: int = Field(title="Порт ДБ", default="5432")
    postgres_db: str = Field(title="Название БД")
    # endregion

    database_url: PostgresDsn | None = Field(title="Ссылка БД", default=None)

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        if self.database_url:
            return self.database_url
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=f"{self.postgres_db}"
        )

    @field_validator("log_level", mode="before")
    @classmethod
    def lower_log_level(cls, v):
        return v.lower()

    class Config:
        env_file = ".env"


settings = Settings()
