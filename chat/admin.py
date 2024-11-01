from django.contrib import admin
from chat.models import ChatGroup, Event, Message

admin.site.register(ChatGroup)
admin.site.register(Event)
admin.site.register(Message)
