from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from game.models import Record


class TestGameView(TestCase):
    def test_game_page(self):
        url_path = reverse('game:game')
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/game.html')

    def test_add_record(self):
        url_path = reverse('game:save_record')
        response = self.client.post(url_path, data={'score': 200})
        self.assertEqual(Record.objects.count(), 0)
        self.assertEqual(response.status_code, 400)
        user = User.objects.create_user(username='test', password='1321sadfsa@')
        self.client.login(username='test', password='1321sadfsa@')
        response2 = self.client.post(url_path, data={'score': 200})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Record.objects.count(), 1)
