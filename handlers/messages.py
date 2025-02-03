from typing import Annotated

from dependency import get_instagram_messages_service
from exception import MessageNotFoundException, MessageNotSent, UserNotFound
from fastapi import APIRouter, Depends, HTTPException, status
from schema import InstagramMessageReadSchema, InstagramSendMessageBodySchema
from service import InstagramMessageService
from settings import settings

router = APIRouter(
    tags=['message']
)


@router.get(
    path='/messages',
    response_model=list[InstagramMessageReadSchema]
)
async def get_messages(
    user_id: int,
    instagram_messages_service: Annotated[
        InstagramMessageService,
        Depends(get_instagram_messages_service)
    ],
    messages_count: int = settings.GET_MESSAGES_DEFAULT_COUNT,
) -> InstagramMessageReadSchema:
    try:
        return instagram_messages_service.get_messages(
            user_id=user_id, messages_count=messages_count
        )
    except MessageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.post(
    path='/message/send',
    response_model=InstagramSendMessageBodySchema,
    status_code=status.HTTP_200_OK
)
async def send_message(
    instagram_message_service: Annotated[
        InstagramMessageService,
        Depends(get_instagram_messages_service)
    ],
    body: InstagramSendMessageBodySchema,
    user_id: int | None = None,
    username: str | None = None,
) -> InstagramSendMessageBodySchema:
    try:
        return instagram_message_service.send_message(
            recipient_id=user_id,
            message=body
        )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except MessageNotSent as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail
        )
