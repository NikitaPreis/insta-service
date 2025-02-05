# Микросерс для работы с Instagram API

### Описание

Проект «insta-service» — это микросервис, реалиализующий работу с Instagram API.
В сервисе реализованы следующие функции:
1. Обработка и сохранение входящих сообщений (подписка на webhook);
2. Получение списка последних сообщений из диалога с пользователем;
3. Получение информации об пользователе;
4. Отправка сообщения в диалог пользователя.


### Стек технологий:

* Python (3.11.9)
* FastAPI
* Pydantic
* Starlette
* Uvicorn
* SQLAlchemy
* Alembic
* PostgreSQL
* Docker

### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git@github.com:NikitaPreis/insta-service.git
cd insta-service
```

Создать и активировать виртуальное окружение:
```
python3 -m venv venv
source venv/Scripts/activate
```

Обновить pip и установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Установить переменные окружения в файле .env:
```
# Переменные окружения для запуска БД (Docker Compose):
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_USER=postgres
POSTGRES_DB=instagram_service
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Переменные окружения для подключения к базе данных (SQLAlchemy, Alembic)
DB_DRIVER=postgresql+psycopg2
DB_PASSWORD=mysecretpassword
DB_USER=postgres
DB_NAME=instagram_service
DB_HOST=localhost
DB_PORT=5432

# Переменные окружения, необходимые для работы с Instagram API
INSTAGRAM_APP_SECRET=<instagram-developer-app-token>
INSTAGRAM_USER_TOKEN=<instagram-user-access-token>
INSTAGRAM_WEBHOOK_TOKEN=<instagram-webhook-access-token>
INSTAGRAM_SEND_MESSAGE_URL=https://graph.instagram.com/v22.0/me/messages
INSTAGRAM_ACCOUNT_ID=<instagram-account-id>
INSTAGRAM_ACCOUNT_SCOPED_ID=<instagram-account-scoped-id>
```

Запустить Docker daemon и ввести команду для запуска БД (PostgreSQL) в контейнере через Docker Compose:
```
docker compose up
```

Запустить сервер, создать и выполнить миграции:
```
fab runserver
fab makemigrations
fab migrate
```

Чтобы сервис принимал принимал webhooks от instagram, установите и запустите туннель, например, от Tuna:
* Скачайте клиент по инструкции: https://my.tuna.am/
```
Команда для windows (PowerShell): winget install --id yuccastream.tuna
Команда для macOS: brew install yuccastream/tap/tuna
Команда для Linux: curl -sSLf https://get.tuna.am | sh
```
* Установите токен:
```
tuna config save-token <YOUR_TUNA_TOKEN>
```
* Запустите туннель командой:
```
tuna http 8080 --domain=<your_domain> --location=<domain_location>
# Или
tuna http 8000 --subdomain=insta-service-test --location=nl
```

### Список доступных эндпоинтов:

1) **Получение списка последних сообщений с пользователем:**
* *url*: http://localhost:8000/messages?user_id={123}
* *Доступные методы*: GET
2) **Получение информации о пользователе по ID:**
* *url*: http://localhost:8000/user?user_id={123}
* *Доступные методы*: GET
3) **Webhook для получения входящих сообщений:**
* *url*: http://localhost:8000/webhook
* *Доступные методы*: GET, POST
4) **Отправка сооббщеня в диалог:**
* *url*: http://localhost:8000/message/send?user_id={123}
* *Доступные методы*: POST
5) **Документация (OpenAPI/Swagger):**
* *url:* http://localhost:8000/docs

### Примеры запросов и ответов:

**Content type**:
```
application/json

```
**request samples №1:**
```
http://localhost:8000/webhook/
# POST
```

**payload №1:**

```
{
  "object": "instagram",
  "entry": [
    {
      "time": 1738336944781,
      "id": "17841472223448520",
      "messaging": [
        {
          "sender":{
            "id": "1667654223855126"
          },
          "recipient": {
            "id": "17841472223448520"
          },
          "timestamp": 1738336944379,
          "message": {
            "mid":"aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDcyMjIzNDQ4NTIwOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI3NjAxOTc3NDU0MDQ5NDQyNTozMjA2NjY1NjcyNjg0NTc1Mjg3NDMyNzgyNzYxMzIyMDg2NAZDZD",
            "text": "test message webhook"
          }
        }
      ]
    }
  ]
}
```

**response samples №1:**
```
{
    "object": "instagram",
    "entry": [
        {
            "id": 17841472223448520,
            "time": 1738336944781,
            "messaging": [
                {
                    "sender": {
                        "id": 1667654223855126
                    },
                    "recipient": {
                        "id": 17841472223448520
                    },
                    "timestamp": "123456789013",
                    "message": {
                        "mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDcyMjIzNDQ4NTIwOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI3NjAxOTc3NDU0MDQ5NDQyNTozMjA2NjY1NjcyNjg0NTc1Mjg3NDMyNzgyNzYxMzIyMDg2NAZDZD",
                        "text": "test message webhook"
                    }
                }
            ]
        }
    ]
}
```

**request samples №2:**
```
http://localhost:8000/webhook?hub.mode=subscribe&hub.challenge=1158201444&hub.verify_token=12345
# GET
```


**response samples №2:**
```
1158201444
```

**request samples №3:**
```
http://localhost:8000/message/send?user_id=<123>
```

**payload №3:**

```
{
    "recipient":{
        "id":"<user_id>"
    },
    "message": {
        "text":"test send text by API"
    }
}
```

**response samples №3:**
```
{
    "recipient": {
        "id": <user_id>
    },
    "message": {
        "text": "test send text by API"
    }
}
```

**request samples №4:**
```
http://localhost:8000/messages?user_id={123}
```

**response samples №4:**
```
[
    {
        "sender_username": "test_user6023",
        "recipient_username": "test_appstestapps",
        "text": "test message webhook"
    },
    {
        "sender_username": "test_user6023",
        "recipient_username": "test_appstestapps",
        "text": "test new save_message logic V3"
    },
    {
        "sender_username": "test_user6023",
        "recipient_username": "test_appstestapps",
        "text": "test webhook fix"
    },
    {
        "sender_username": "test_appstestapps",
        "recipient_username": "test_user6023",
        "text": "test keyword response"
    },
    {
        "sender_username": "test_appstestapps",
        "recipient_username": "test_user6023",
        "text": "test send text by API"
    }
]
```

**request samples №5:**
```
http://localhost:8000/user?user_id={user_id}
```

**response samples №5:**
```
{
    "id": <user_id>,
    "username": "test_user6023",
    "name": "Test Userr",
    "profile_pic": null,
    "follower_count": 0,
    "is_user_follow_business": true,
    "is_business_follow_user": false
}
```

### Как настроить работу сервиса с Instagram-аккаунтом с помощью туннелирования:

1. Подготовьте аккаунты Meta:
* Разверните instagram-service;
* Зарегистрируйте аккаунт instagram;
* Зарегистрируйте аккаунт facebook;
* Перевидите аккаунт instagram в состояние: бизнес-аккаунт;
* Свяжите аккаунты instagram и facebook;
* Создайте аккаунт разработчика Meta;

2. Подготовьте туннель (например, с помощью Ngrok или Tuna):
* Установите ПО;
* Зарезервируйте статичный домен;
* Проведите туннель между вашим статичным доменом и 0.0.0.0:8000

3. Настройте приложение в аккаунте разработчика Meta:
* Создайте приложение (категория: "бизнес");
* В настройках приложения установите необходимые поля;
* В панели приложения выберите найдите Instagram и кликните по кнопке "настроить";
* В настройке продукта Instagram сгенерируйте маркеры доступа;
* Настройте webhooks;
* Подпишитесь на webhook messages;
* Настройте вход в Instagtam от имени компании;
* Перенесите в соответсвующие переменные .env-файла:
1) Access token пользователя instagram;
2) Access token, который вы использовали для того, чтобы настроить webhook;
3) ID приложения в Instagram;
4) Секрет приложения Instagram;
5) ID вашего аккаунта Instagram;
6) Instagram-scoped ID вашего аккаунта Instagram (Можно найти в теле запроса [поле recipient_id], когда Instagram API отправляет post-запрос к точке /webhook/).

### Направления по доработке сервиса:
1. Переписать код в асинхронной парадигме (asyncio, aiohttp), чтобы ускорить работу сервиса за счет конкурентных запросов к БД и Instagram API;
2. Добавить валидацию для полезной нагрузки, чтобы верифицировать get-запросы к webhook от Instagram (SHA256);
3. Провести рефакторинг для того, чтобы привести API сервиса к состоянию RESTful;
4. Добавить валидацию для схем.
