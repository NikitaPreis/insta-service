from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_PASSWORD: str = 'mysecretpassword'
    DB_USER: str = 'postgres'
    DB_NAME: str = 'instagram_service'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432

    CONTENT_TYPE_JSON_HEADER: str = 'application/json'
    GET_MESSAGES_DEFAULT_COUNT: int = 50

    INSTAGRAM_ACCOUNT_ID: int = 12345
    INSTAGRAM_USER_TOKEN: str = '12345'
    INSTAGRAM_WEBHOOK_TOKEN: str= '12345'
    INSTAGRAM_APP_SECRET: str = 12345
    INSTAGRAM_SEND_MESSAGE_URL: str = ('https://graph.instagram.com/v22.0/'
                                       'me/messages')
    INSTAGRAM_GET_USER_BASE_URL: str = 'https://graph.instagram.com/v22.0/'
    INSTAGRAM_GET_USER_FIELDS: str = ('id,name,username,'
                                      'profile_pic,'
                                      'follower_count,'
                                      'is_user_follow_business,'
                                      'is_business_follow_user')

    @property
    def db_url(self):
        return (f'{self.DB_DRIVER}://{self.DB_USER}:'
                f'{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')

    @property
    def instagram_send_message_headers(self):
        return {
            'Authorization': f'Bearer {self.INSTAGRAM_USER_TOKEN}',
            'Content-Type': self.CONTENT_TYPE_JSON_HEADER
        }

settings = Settings()
