from dataclasses import dataclass

from clients import InstagramClient
from exception import MessageNotFoundException, UserNotFound
from models import InstagramMessage
from repository import InstagramMessageRepository, UserRepository
from schema import (InstagramMessageReadSchema, InstagramSendMessageBodySchema,
                    InstagramUserProfileSchema)
from settings import Settings


@dataclass
class InstagramMessageService:
    message_repository: InstagramMessageRepository
    user_repository: UserRepository
    instagram_client: InstagramClient
    settings: Settings

    def get_messages(self, user_id: int, messages_count: int):
        user_profile_schema = self.instagram_client.get_user(
            user_id=user_id
        )
        company_profile_schema = self.instagram_client.get_user(
            self.settings.INSTAGRAM_ACCOUNT_ID
        )
        messages = self.message_repository.get_messages(
            user_id=user_id
        )[-messages_count:]
        if not messages:
            raise MessageNotFoundException
        if not user_profile_schema or not company_profile_schema:
            raise UserNotFound
        readable_messages = self._converte_messages_into_readable_ones(
            messages=messages, user_profile_schema=user_profile_schema,
            company_profile_schema=company_profile_schema
        )
        return readable_messages

    def send_message(
        self, recipient_id: int, message: InstagramSendMessageBodySchema
    ) -> InstagramSendMessageBodySchema:
        message = self.instagram_client.send_text_message(
            recipient_id=recipient_id, text=message.message.text
        )
        return message

    def _converte_messages_into_readable_ones(
        self, messages: list[InstagramMessage],
        user_profile_schema: InstagramUserProfileSchema,
        company_profile_schema: InstagramUserProfileSchema
    ) -> list[InstagramMessageReadSchema]:
        readable_messages = []
        for current_message in messages:
            if current_message.sender_id == user_profile_schema.id:
                message = InstagramMessageReadSchema(
                    sender_username=user_profile_schema.username,
                    recipient_username=company_profile_schema.username,
                    text=current_message.text
                )
            else:
                message = InstagramMessageReadSchema(
                    sender_username=company_profile_schema.username,
                    recipient_username=user_profile_schema.username,
                    text=current_message.text
                )
            readable_messages.append(message)
        return readable_messages

    def _set_message_recipient_id(
        self, recipient_id: int,
        message: InstagramSendMessageBodySchema
    ) -> InstagramSendMessageBodySchema:
        message.recipient.id = recipient_id
        print(message)
        return message
