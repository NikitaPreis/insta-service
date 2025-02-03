from datetime import datetime 
from typing import Any

from pydantic import BaseModel, Field


# class InstagramMessageReadSchema(BaseModel):
#     # Должен быть username
#     sender_name: str
#     recipient_name: str
#     text: str


class InstagramMessageReadSchema(BaseModel):
    # Должен быть username
    sender_username: str
    recipient_username: str
    text: str

    def __str__(self):
        return (f'{self.sender_username} -> {self.recipient_username}: '
                f'{self.text}')


# class InstagramMessageReadSchema(BaseModel):
#     # Должен быть username
#     recipient_id: int
#     text: str


class InstagramSendMessageRecipient(BaseModel):
    id: int


class InstagramChatReadSchema(BaseModel):
    # Должны быть usernames
    sender_id: int
    message: InstagramMessageReadSchema


class InstagramSendMessageSchema(BaseModel): 
    text: str


class InstagramSendMessageBodySchema(BaseModel):
    recipient: InstagramSendMessageRecipient | None = None
    message: InstagramSendMessageSchema
