from dataclasses import dataclass

from clients import InstagramClient
from exception import TokenNotCorrect, UserNotFound
from repository import InstagramMessageRepository, UserRepository
from settings import Settings
from service import InstagramUserService
from schema import InstagramNewMessageDataSchema


@dataclass
class InstagramWebhookService:
    message_repository: InstagramMessageRepository
    # user_repository: UserRepository,
    instagram_user_service: InstagramUserService
    instagram_client: InstagramClient
    settings: Settings


    def verify_request(
        self, hub_mode: str,
        hub_challenge: int,
        hub_verify_token: str
    ):
        """Вебхук для верификации приложения в Instagram API.
        
        Принимает параметры:
        1) hub_mode (Значение всегда subscribe);
        2) hub_challenge (Числовой код, который необходимо
                                    отправить обратно API);
        3) hub_verify_token (Токен, заданный на доске приложений
                            в конифгирации вебхук Instagram API.
                            Используется для проверки запроса:
                            убеждаемся, что запрос отправлен Instagram API).
        """
        if hub_verify_token != self.settings.INSTAGRAM_WEBHOOK_TOKEN:
            raise TokenNotCorrect
        return int(hub_challenge)

    def save_message(
        self, message_data: InstagramNewMessageDataSchema
    ):
        self.instagram_user_service.create_user_if_not_exist_id_only(
            message_data.sender.id
        )
        self.instagram_user_service.create_user_if_not_exist_id_only(
            message_data.recipient.id
        )
        self.message_repository.save_message(
            message=message_data
        )
        return message_data

    # def _create_user_if_not_exist(self, user_id: int) -> int:
    #     if not self.user_repository.get_user(user_id=user_id):
    #         instagram_user_schema = self.instagram_client.get_user(
    #             user_id=user_id
    #         )
    #         if not instagram_user_schema:
    #             raise UserNotFound
    #         self.user_repository.create_user(
    #             user_id=instagram_user_schema.id,
    #             username=instagram_user_schema.username
    #         )
    #     return user_id

    # save_massage?
    # def create_message(
    #     self, message_data: InstagramNewMessageDataSchema
    # ):
    #     user_id = message_data.sender.id
    #     if not self.user_repository.get_user(
    #         user_id=user_id
    #     ):
    #         self.user_repository.create_user(user_id=user_id)
    #     message_id = self.message_repository.save_message(
    #         user_id=user_id, message=message_data
    #     )
    #     # message = self.message_repository.get_message(message_id=message_id)
    #     return message_data
