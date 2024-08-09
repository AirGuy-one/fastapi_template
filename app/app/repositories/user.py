from .base import RepositoryBase
from app.models.user import User


class RepositoryUser(RepositoryBase[User]):
    ...
