from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class InstagramMessage(Base):
    __tablename__ = 'instagram_messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    sent_time: Mapped[int] = mapped_column(DateTime, nullable=False)
    mid: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    sender_id: Mapped[str] = mapped_column(
        ForeignKey('instagram_user_profiles.id'), nullable=False
    )
    recipient_id: Mapped[str] = mapped_column(
        ForeignKey('instagram_user_profiles.id'), nullable=False
    )
