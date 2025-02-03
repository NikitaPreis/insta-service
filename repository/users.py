from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import InstagramUserProfile
from schema import InstagramUserProfileSchema


@dataclass
class UserRepository:
    db_session: Session


    def get_user(self, user_id: int) -> InstagramUserProfile | None:
        query = select(InstagramUserProfile).where(
            InstagramUserProfile.id == user_id
        )
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def create_user_id_only(
        self, user_id: int
    ) -> InstagramUserProfile:
        query = insert(InstagramUserProfile).values(
            id=user_id
        ).returning(InstagramUserProfile.id)
        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            return self.get_user(user_id)

    def create_user(
        self, user_id: int, username: str
    ) -> InstagramUserProfile:
        query = insert(InstagramUserProfile).values(
                id=user_id, #username=username
        ).returning(InstagramUserProfile.id)
        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            return self.get_user(user_id)

    def get_user_by_username(self, username: str) -> InstagramUserProfile | None:
        query = select(InstagramUserProfile).where(
            InstagramUserProfile.username == username
        )
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()
