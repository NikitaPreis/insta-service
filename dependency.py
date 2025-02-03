from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from clients import InstagramClient
from database import get_db_session
from repository import InstagramMessageRepository, UserRepository
from service import (InstagramMessageService, InstagramUserService,
                     InstagramWebhookService)
from settings import Settings


def get_instagram_message_repository(
    db_session: Annotated[Session, Depends(get_db_session)]
) -> InstagramMessageRepository:
    return InstagramMessageRepository(db_session=db_session)


def get_user_repository(
    db_session: Annotated[Session, Depends(get_db_session)]
):
    return UserRepository(db_session=db_session)


def get_instagram_client() -> InstagramClient:
    return InstagramClient(settings=Settings())


def get_instagram_user_service(
    user_repository: Annotated[
        UserRepository, Depends(get_user_repository)
    ],
    instagram_client: Annotated[
        InstagramClient, Depends(get_instagram_client)
    ]
) -> InstagramUserService:
    return InstagramUserService(
        user_repository=user_repository,
        instagram_client=instagram_client,
        settings=Settings()
    )


def get_instagram_messages_service(
    message_repository: Annotated[InstagramMessageRepository,
                                  Depends(get_instagram_message_repository)],
    user_repository: Annotated[UserRepository,
                               Depends(get_user_repository)],
    instagram_client: Annotated[InstagramClient,
                                Depends(get_instagram_client)]
) -> InstagramMessageService:
    return InstagramMessageService(
        settings=Settings(),
        message_repository=message_repository,
        user_repository=user_repository,
        instagram_client=instagram_client
    )


def get_instagram_webhook_service(
    message_repository: Annotated[
        InstagramMessageRepository,
        Depends(get_instagram_message_repository)
    ],
    instagram_user_service: Annotated[
        InstagramUserService,
        Depends(get_instagram_user_service)
    ],
    instagram_client: Annotated[InstagramClient,
                                Depends(get_instagram_client)]
) -> InstagramWebhookService:
    return InstagramWebhookService(
        settings=Settings(),
        message_repository=message_repository,
        instagram_user_service=instagram_user_service,
        instagram_client=instagram_client
    )
