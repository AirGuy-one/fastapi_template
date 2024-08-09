from dependency_injector import containers, providers

from app.core.config import Settings
from app.db.session import SyncSession

from app.models.user import User

from app.repositories.user import RepositoryUser

from app.services.user import UserService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession, db_url=config.provided.postgres_url)
    session = providers.Factory(db().create_session)

    # region repository
    repository_user = providers.Singleton(RepositoryUser, model=User, session=session)
    # endregion

    # region services
    user_service = providers.Singleton(UserService, repository_user=repository_user)
    # endregion
