import json
from channels.generic.websocket import WebsocketConsumer
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

    def disconnect(self, code):
        print('disconnect')
