from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from models import InstagramMessage
from schema import InstagramNewMessageDataSchema


class InstagramMessageRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_messages(self, user_id) -> list[InstagramMessage]:
        query = select(InstagramMessage).where(
            (InstagramMessage.sender_id == user_id) |
            (InstagramMessage.recipient_id == user_id)
        ).order_by(InstagramMessage.sent_time)
        with self.db_session() as session:
            messages: list[InstagramMessage] = session.execute(query).scalars().all()
            return messages

    def save_message(
        self, message: InstagramNewMessageDataSchema
    ) -> int:
        print(message)
        message_model = InstagramMessage(
            sent_time = message.timestamp,
            mid = message.message.mid,
            text = message.message.text,
            sender_id = message.sender.id,
            recipient_id = message.recipient.id
        )
        with self.db_session() as session:
            session.add(message_model)
            session.commit()
            return message_model.id
