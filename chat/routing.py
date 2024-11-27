from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('chat/groups/', consumers.LeaveJoinConsumer.as_asgi()),
    path('chat/group/<uuid:uuid>/', consumers.ChatConsumer.as_asgi()),
]