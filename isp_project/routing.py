from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from kuhub.consumers import NotificationConsumer
from django.urls import path

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # your routing configuration for websockets
            path("ws/notifications/", NotificationConsumer.as_asgi()),
        )
    ),
})
