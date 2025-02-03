from datetime import datetime 
from typing import Any

from pydantic import BaseModel, Field


class InstagramNewMessageSenderSchema(BaseModel):
    id: int


class InstagramNewMessageRecipientSchema(BaseModel):
    id: int


class InstagramMessageSchema(BaseModel):
    mid: str
    text: str


class InstagramNewMessageDataSchema(BaseModel):
    sender: InstagramNewMessageSenderSchema
    recipient: InstagramNewMessageRecipientSchema
    timestamp: datetime # datetime
    message: InstagramMessageSchema


class InstagramMessageEntrySchema(BaseModel):
    id: int # str?
    time: int
    messaging: list[InstagramNewMessageDataSchema]

# CHANGES - FIELD VALUE
# class InstagramNewMessageSchema(BaseModel):
#     field: str
#     value: InstagramNewMessageDataSchema

# CHANGES
# class InstagramMessageEntrySchema(BaseModel):
#     id: int # str?
#     time: int
#     changes: list[InstagramNewMessageSchema]


class InstagramMessageSchema(BaseModel):
    object: str
    entry: list[InstagramMessageEntrySchema]


# class TestMessage(BaseModel):
#     object: Any
#     entry: Any


class MessageCreateSchema(BaseModel):
    pass

