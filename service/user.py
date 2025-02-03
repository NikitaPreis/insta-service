from dataclasses import dataclass

from clients import InstagramClient
from exception import UserNotFound
from repository import UserRepository
from schema import InstagramUserProfileSchema
from settings import Settings


@dataclass
class InstagramUserService:
    settings: Settings
    user_repository: UserRepository
    instagram_client: InstagramClient

    def get_user_from_instagram(
        self, user_id: int | None, username: str | None
    ) -> InstagramUserProfileSchema:
        user_schema = self.instagram_client.get_user(
            user_id=user_id
        )
        return user_schema

    def create_user_if_not_exist_id_only(self, user_id: int) -> int:
        if self.user_repository.get_user(user_id=user_id):
            return user_id
        self.user_repository.create_user_id_only(
            user_id=user_id
        )
        return user_id

    def create_user_if_not_exist(self, user_id: int) -> int:
        if not self.user_repository.get_user(user_id=user_id):
            instagram_user_schema = self.instagram_client.get_user(
                user_id=user_id
            )
            if not instagram_user_schema:
                raise UserNotFound
            self.user_repository.create_user(
                user_id=instagram_user_schema.id,
                username=instagram_user_schema.username
            )
        return user_id
