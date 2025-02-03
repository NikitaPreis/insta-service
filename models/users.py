from typing import Optional

from sqlalchemy import BigInteger, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class InstagramUserProfile(Base):
    __tablename__ = 'instagram_user_profiles'

    id: Mapped[int] = mapped_column(
        BigInteger,
        #
        primary_key=True, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        nullable=True
    )
    username: Mapped[str] = mapped_column(
        nullable=True, unique=True
    )
    profile_pic: Mapped[str] = mapped_column(
        nullable=True
    )
    follower_count: Mapped[str] = mapped_column(
        nullable=True
    )
    is_user_follow_business: Mapped[bool] = mapped_column(
        nullable=True
    )
    is_business_follow_user: Mapped[bool] = mapped_column(
        nullable=True
    )


# class UserProfile(Base):
#     __tablename__ = 'user_profiles'

#     id: Mapped[int] = mapped_column(
#         BigInteger,
#         #
#         primary_key=True, nullable=False, unique=True
#     )
#     username: Mapped[str] = mapped_column(
#         nullable=True, unique=True
#     )
