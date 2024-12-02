import os

from channels.auth import AuthMiddlewareStack

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    "http": app,
    "websocket":
        AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(chat.routing.websocket_urlpatterns)
            ),
        )
})
