from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from vcars.models import Pic


class PicTests(APITestCase):
    def test_get_pic_list(self):
        response = self.client.get(reverse('api_vcars:list-pics'), format='json')
        assert response.data['count'] == Pic.objects.count()

