from uuid import  UUID

from app.repositories.user import RepositoryUser
from app.schemas.user import UserSchema


class UserService:

    def __init__(self, repository_user: RepositoryUser) -> None:
        self._repository_user = repository_user

    async def get_user(self, user_id: UUID) -> UserSchema:
        user = self._repository_user.get(id=user_id)
        return UserSchema(**user.to_dict(include_relationships=False))

    async def list_users(self) -> list[UserSchema]:
        return [
            UserSchema(**user.to_dict(include_relationships=False))
            for user in self._repository_user.list()
        ]
