from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('chat/groups/', consumers.LeaveJoinConsumer.as_asgi()),
]