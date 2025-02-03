from pydantic import BaseModel


class InstagramMessageReadSchema(BaseModel):
    sender_username: str
    recipient_username: str
    text: str

    def __str__(self):
        return (f'{self.sender_username} -> {self.recipient_username}: '
                f'{self.text}')


class InstagramSendMessageRecipient(BaseModel):
    id: int


class InstagramChatReadSchema(BaseModel):
    sender_id: int
    message: InstagramMessageReadSchema


class InstagramSendMessageSchema(BaseModel):
    text: str


class InstagramSendMessageBodySchema(BaseModel):
    recipient: InstagramSendMessageRecipient | None = None
    message: InstagramSendMessageSchema
