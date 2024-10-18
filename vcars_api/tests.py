from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from config.settings import BASE_DIR
from vcars.models import Pic


class PicTests(APITestCase):
    def create_pic_and_post(self):
        img = open(BASE_DIR / 'media/default.png', 'rb')
        url = reverse('api_vcars:add-pic')
        data = {'name': 'mcqueen', 'body': 'pixar cars', 'tags': ['12', '22', 'cars'], 'pic': img}
        response = self.client.post(url, data=data)

        return response

    def test_get_pic_list(self):
        response = self.client.get(reverse('api_vcars:list-pics'), format='json')
        assert response.data['count'] == Pic.objects.count()

    def test_add_pic(self):
        response = self.create_pic_and_post()
        assert response.status_code == HTTP_201_CREATED

    def test_add_comment(self):
        url = reverse('api_vcars:write-comment')
        self.create_pic_and_post()
        response1 = self.client.post(url, data={'body': 'asfasfsafxz', 'name': 'jonny', 'pic': 1})
        response2 = self.client.post(url, data={'body': 'asfasfsafxz', 'name': 'jonny', 'pic': 2})
        assert response1.status_code == HTTP_201_CREATED
        assert response2.status_code == HTTP_400_BAD_REQUEST
