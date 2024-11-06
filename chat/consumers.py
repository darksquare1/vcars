import json

from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from chat.models import ChatGroup, Event, Message


class LeaveJoinConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        if action_type := text_data.get('type'):
            data = text_data.get('data')
            if action_type == 'leave_group':
                self.leave_group(data)
            elif action_type == 'join_group':
                self.join_group(data)

    def leave_group(self, group_uuid):
        ChatGroup.objects.get(uuid=group_uuid).remove_user_from_group(self.user)
        self.send(json.dumps(dict(type='leave_group', data=group_uuid)))

    def join_group(self, group_uuid):
        ChatGroup.objects.get(uuid=group_uuid).add_user_to_group(self.user)
        self.send(json.dumps(dict(type='join_group', data=group_uuid)))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_uuid = str(self.scope['url_route']['kwargs']['uuid'])
        self.group = await database_sync_to_async(ChatGroup.objects.get)(uuid=self.group_uuid)
        await self.channel_layer.group_add(self.group_uuid, self.channel_name)
        self.user = self.scope['user']
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        action_type = text_data.get('type')
        message = text_data.get('message')
        author = text_data.get('author')
        if action_type == 'text_message':
            user = await database_sync_to_async(User.objects.get)(username=author)
            message = await database_sync_to_async(Message.objects.create)(author=user, body=message,
                                                                           group=self.group)
        await self.channel_layer.group_send(self.group_uuid, {
            'type': 'text_message',
            'message': str(message),
            'author': author
        })

    async def text_message(self, event):
        message = event['message']
        returned_data = dict(type='text_message', message=message, group_uuid=self.group_uuid)
        await self.send(json.dumps(returned_data))


