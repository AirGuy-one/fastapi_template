from uuid import UUID

from fastapi import APIRouter, Depends, status

from dependency_injector.wiring import Provide, inject

from app.services.user import UserService
from app.schemas.user import UserSchema

from app.core.container import Container
from app.core.logger import SafeLoggingRoute
from app.api.deps import commit_and_close_session
from app.api.pagination import PaginationParams, Paginator, BasePaginationResponse

router = APIRouter(route_class=SafeLoggingRoute)


@router.get(
    "/user",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user",
    description="This endpoints retrieve user"
)
@inject
@commit_and_close_session
async def get_user(
        user_id: UUID, user_service: UserService = Depends(Provide[Container.user_service])
) -> UserSchema:
    return await user_service.get_user(user_id=user_id)


@router.get(
    "/users",
    response_model=BasePaginationResponse[UserSchema],
    status_code=status.HTTP_200_OK,
    summary="Get user",
    description="TThis endpoint retrieves all the users"
)
@inject
@commit_and_close_session
async def list_users(
        user_service: UserService = Depends(Provide[Container.user_service]),
        pagination: PaginationParams = Depends(PaginationParams)
) -> BasePaginationResponse[UserSchema]:
    response = await user_service.list_users()
    paginator = Paginator(data=response, pagination_params=pagination)
    return paginator.get_response()


