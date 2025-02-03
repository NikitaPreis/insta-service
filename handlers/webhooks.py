from typing import Annotated

from fastapi import APIRouter, Body, Query, Depends, HTTPException, status
from fastapi.requests import Request
import requests

from dependency import get_instagram_webhook_service
from exception import TokenNotCorrect
from service import InstagramWebhookService
from settings import Settings
from schema import InstagramMessageSchema


router = APIRouter(
    prefix='/webhook'
)


@router.get('')
async def webhook(
    instagram_webhook_service: Annotated[
        InstagramWebhookService, 
        Depends(get_instagram_webhook_service)
    ],
    hub_mode : Annotated[str, Query(alias='hub.mode')],
    hub_challenge : Annotated[int, Query(alias='hub.challenge')],
    hub_verify_token : Annotated[str, Query(alias='hub.verify_token')]
) -> int:
    print('VERIFY')
    try:
        return instagram_webhook_service.verify_request(
            hub_mode=hub_mode, hub_challenge=hub_challenge,
            hub_verify_token=hub_verify_token
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.post(
    '',
    response_model=InstagramMessageSchema
)
async def webhook(
    instagram_webhook_service: Annotated[
        InstagramWebhookService, 
        Depends(get_instagram_webhook_service)
    ],
    body: InstagramMessageSchema,
) -> InstagramMessageSchema:
    instagram_webhook_service.save_message(
        message_data=body.entry[0].messaging[0]
    )
    return body
