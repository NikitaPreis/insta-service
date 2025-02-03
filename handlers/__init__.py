from handlers.messages import router as message_router
from handlers.users import router as user_router
from handlers.webhooks import router as webhook_router

routers = [message_router, user_router, webhook_router]
