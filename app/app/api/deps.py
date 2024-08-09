from functools import wraps

from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from dependency_injector.wiring import inject, Provide

from app.repositories.user import RepositoryUser
from app.core.container import Container
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/login")


@inject
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        repository_user: RepositoryUser = Depends(Provide[Container.repository_user])
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("login")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = repository_user.get(login=username)
    if user is None:
        raise credentials_exception
    return user


@inject
def commit_and_close_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = Container.session()
        try:
            result = await func(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return wrapper
