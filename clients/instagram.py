from dataclasses import dataclass
import requests

from exception import MessageNotSent, UserDataNotAvailable
from schema import (InstagramSendMessageSchema,
                    InstagramSendMessageBodySchema,
                    InstagramSendMessageRecipient,
                    InstagramUserProfileSchema)
from settings import Settings


@dataclass
class InstagramClient:
    settings: Settings


    def get_user(self, user_id: int) -> InstagramUserProfileSchema:
        url = self._get_instagram_user_url(user_id=user_id)
        response = requests.get(url=url)
        if (response.ok
            and self.settings.CONTENT_TYPE_JSON_HEADER
            in response.headers.get('Content-Type'), ''):
                user_data = response.json()
                user_schema = InstagramUserProfileSchema(**user_data)
                return user_schema
        raise UserDataNotAvailable

    def send_text_message(
        self, recipient_id: int, text: str
    ) -> InstagramSendMessageBodySchema:
        url = self.settings.INSTAGRAM_SEND_MESSAGE_URL
        headers = self.settings.instagram_send_message_headers
        message_data = self._get_text_message_data(
            recipient_id=recipient_id, text=text
        )
        response = requests.post(
            url=url,
            headers=headers,
            json=message_data
        )
        if response.status_code != 200:
            raise MessageNotSent
        message_schema = InstagramSendMessageBodySchema(
            recipient=InstagramSendMessageRecipient(id=recipient_id),
            message=InstagramSendMessageSchema(text=text)
        )
        return message_schema

    def _get_instagram_user_url(self, user_id: int):
        if user_id == self.settings.INSTAGRAM_ACCOUNT_ID:
            request_user_fields = 'id,name,username'
        else:
            request_user_fields = self.settings.INSTAGRAM_GET_USER_FIELDS
        return (
            f'{self.settings.INSTAGRAM_GET_USER_BASE_URL}{user_id}'
            f'?fields={request_user_fields}'
            f'&access_token={self.settings.INSTAGRAM_USER_TOKEN}'
        )

    def _get_text_message_data(self, recipient_id: int, text: str):
        return {
            'recipient': {
                'id': recipient_id
            },
            'message':{
                'text': text
            }
        }
