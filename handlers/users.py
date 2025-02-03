from typing import Annotated

from dependency import get_instagram_user_service
from exception import UserDataNotAvailable, UserNotFound
from fastapi import APIRouter, Depends, HTTPException, status
from schema import InstagramUserProfileSchema
from service import InstagramUserService

router = APIRouter(
    prefix='/user',
    tags=['message']
)


@router.get(
    path='/',
    response_model=InstagramUserProfileSchema
)
async def get_user(
    user_service: Annotated[InstagramUserService,
                            Depends(get_instagram_user_service)],
    user_id: int | None,
    username: str | None = None
) -> InstagramUserProfileSchema:
    try:
        return user_service.get_user_from_instagram(
            user_id=user_id, username=username
        )
    except UserDataNotAvailable as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
