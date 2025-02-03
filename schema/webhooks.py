from datetime import datetime

from pydantic import BaseModel


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
    timestamp: datetime
    message: InstagramMessageSchema


class InstagramMessageEntrySchema(BaseModel):
    id: int
    time: int
    messaging: list[InstagramNewMessageDataSchema]


class InstagramMessageSchema(BaseModel):
    object: str
    entry: list[InstagramMessageEntrySchema]
