from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from dependency import get_instagram_messages_service
from exception import (MessageNotFoundException,
                       UserNotFound, MessageNotSent)
from service import InstagramMessageService
from settings import settings
from schema import (InstagramMessageReadSchema,
                    InstagramSendMessageBodySchema)


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
): #-> InstagramMessageReadSchema:
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
):
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

    
    # return response.status_code

### full_access_token:
# access_token = 'EAANw5GpG4HkBO3pEWSaLLF39UgTkJZBoNm50muyM3biovfZBvH9M6vYb47hTZCG2xSEKNJt8Ka1NoXDiZA5TWU6Hu5vTh7vNoTfbideTonNdt9nLwvwTaQYnMR4rCggcK9reUjYruOZApPzk06lLSZCFPpkRCsaDOcq849B8yQ87lEekeEdvbsxGZASENsZAA65U'
### instagram_token:
# access_token = 'IGAAIWZBfLec4tBZAFA1SUpxWnZAselNMQXBISTgzZAGVKNFB1VlZAyNkFaZAE1kYnZA5RWJMT3F1aUVxVVd2M2N2YXFCT2ZACdlpOMTRxLTBmV2xKWENkQTExaWRNcFVRSXRBdWFRRm9uc1VNbHo2cXMtRUYzaTdacHBVRzdsZAmlYTkE0cwZDZD'
### instagram_token_latest
