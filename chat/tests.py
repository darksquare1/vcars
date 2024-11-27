import pytest
from channels.db import database_sync_to_async
from django.test import TestCase, Client
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.urls import reverse

from chat.models import ChatGroup
from chat.consumers import LeaveJoinConsumer, ChatConsumer
from accounts.tests import UserCreationMixin


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio()
async def test_leave_join_consumer():
    user = await database_sync_to_async(User.objects.create_user)(username='mcqueen', password='asdasdxzcxz1312')
    group = await database_sync_to_async(ChatGroup.objects.create)(name='Test Group',
                                                                   uuid='123e4567-e89b-12d3-a456-426614174000')
    await database_sync_to_async(group.members.add)(user)
    communicator = WebsocketCommunicator(LeaveJoinConsumer.as_asgi(), "/chat/groups/")
    communicator.scope['user'] = user
    connected, _ = await communicator.connect()
    assert connected
    leave_message = {
        'type': 'leave_group',
        'data': '123e4567-e89b-12d3-a456-426614174000'
    }
    await communicator.send_json_to(leave_message)
    response = await communicator.receive_json_from()
    assert response['type'] == 'leave_group'
    assert response['data'] == '123e4567-e89b-12d3-a456-426614174000'
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_consumer():
    user1 = await database_sync_to_async(User.objects.create_user)(username='user1', password='password421421412')
    user2 = await database_sync_to_async(User.objects.create_user)(username='user2', password='passwordцкйкйц14')
    group = await database_sync_to_async(ChatGroup.objects.create)(name='Test Group',
                                                                   uuid='123e4566-e89b-12d3-a456-426614174000')
    await database_sync_to_async(group.members.add)(user1)
    await database_sync_to_async(group.members.add)(user2)
    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(),
        f"/chat/groups/{group.uuid}/"
    )
    communicator.scope['user'] = user1
    communicator.scope['url_route'] = {'kwargs': {'uuid': group.uuid}}
    connected, _ = await communicator.connect()
    assert connected
    message_data = {
        'type': 'text_message',
        'message': 'Hello, user2!',
        'author': user1.username
    }
    await communicator.send_json_to(message_data)
    response = await communicator.receive_json_from()
    assert response['type'] == 'text_message'
    assert 'Hello, user2!' in response['message']
    communicator2 = WebsocketCommunicator(
        ChatConsumer.as_asgi(),
        f"/chat/groups/{group.uuid}/"
    )
    communicator2.scope['user'] = user2
    communicator2.scope['url_route'] = {'kwargs': {'uuid': group.uuid}}
    connected2, _ = await communicator2.connect()
    assert connected2
    message_data = {
        'type': 'text_message',
        'message': 'Hello, user1!',
        'author': user2.username
    }
    await communicator2.send_json_to(message_data)
    response2 = await communicator.receive_json_from()
    assert response2['type'] == 'text_message'
    assert 'Hello, user1!' in response2['message']
    await communicator.disconnect()
    await communicator2.disconnect()


class TestGroupList(UserCreationMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().create_user()

    def test_grouplist_page(self):
        self.client.login(username=self.username, password=self.password)
        url_path = reverse('chat:group_list')
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/groups_list.html')
        response2 = self.client.post(url_path, data={'name': 'Backend chat'})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(ChatGroup.objects.count(), 1)
        self.client.logout()
        response3 = self.client.get(url_path)
        self.assertEqual(response3.status_code, 302)


class TestGroupDetail(UserCreationMixin, TestCase):
    def test_groupdetail_page(self):
        user1 = User.objects.create_user(username='test1', password='dasldas1@das')
        user2 = User.objects.create_user(username='test2', password='2dasldas1dasz')
        group = ChatGroup.objects.create(name='Backend')
        client1 = Client()
        client1.login(username=user1.username, password='dasldas1@das')
        client2 = Client()
        client2.login(username=user2.username, password='2dasldas1dasz')
        group.members.add(user1, user2)
        url_path = reverse('chat:group_detail', args=[group.uuid])
        response = client1.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('chat/group_detail.html')
        client2.logout()
        response2 = client2.get(url_path)
        self.assertEqual(response2.status_code, 302)
