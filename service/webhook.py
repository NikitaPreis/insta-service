from dataclasses import dataclass

from clients import InstagramClient
from exception import TokenNotCorrect
from repository import InstagramMessageRepository
from schema import InstagramNewMessageDataSchema
from service import InstagramUserService
from settings import Settings


@dataclass
class InstagramWebhookService:
    message_repository: InstagramMessageRepository
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
