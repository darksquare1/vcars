import time
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Manager
from django.test import TestCase

from config.settings import BASE_DIR
from vcars.models import Pic


class TestModelPic(TestCase):
    def setUp(self):
        self.img = open(BASE_DIR / 'media/default.png', 'rb')
        self.default_picture = SimpleUploadedFile(
            name='default.png',
            content=self.img.read(),
            content_type='image/png'
        )
        self.pic = Pic(
            pk=1,
            name='Car pic',
            body='Test body for pic',
            pic=self.default_picture
        )
        self.pic.tags.add('mcqueen', 'car')
        self.pic.save()

    def test_create_pic(self):
        self.assertIsInstance(self.pic, Pic)

    def test_str_representation(self):
        self.assertEqual(str(self.pic), 'Car pic')

    def test_slug_is_not_empty(self):
        self.assertTrue(self.pic.slug)

    def test_pic_path_is_not_empty(self):
        self.assertTrue(self.pic.pic.path)

    def test_retrieve_and_save_pics(self):
        pic1 = Pic(
            pk=2,
            name='Car pic 2',
            body='Test body for pic',
            pic=self.default_picture
        )
        pic1.save()
        time.sleep(0.01)
        pic2 = Pic(
            pk=3,
            name='Car pic 3',
            body='Test body for pic',
            pic=self.default_picture
        )
        pic2.save()
        saved_pics = Pic.objects.exclude(pk=1)
        self.assertEqual(saved_pics.count(), 2)
        first_pic = saved_pics[0]
        second_pic = saved_pics[1]
        self.assertEqual(first_pic.name, 'Car pic 3')
        self.assertEqual(second_pic.name, 'Car pic 2')

    def test_model_managers(self):
        self.assertIsInstance(Pic.custom, Manager)
        self.assertIsInstance(Pic.objects, Manager)

    def test_pic_extension(self):
        path = self.pic.pic.path.split('.')[1]
        self.assertIn(path, ['jpg', 'webp', 'jpeg', 'png'])

    def setDown(self):
        self.img.close()
