import time
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Manager
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from config.settings import BASE_DIR
from vcars.models import Pic
from vcars.views import PictureListView, PicDetailView, CreatePic
from vcars.forms import PicForm


class PicCreationMixin:
    @classmethod
    def create_pic(cls):
        cls.img = open(BASE_DIR / 'media/default.png', 'rb')
        cls.default_picture = SimpleUploadedFile(
            name='default.png',
            content=cls.img.read(),
            content_type='image/png'
        )
        cls.pic = Pic(
            name='Car pic',
            body='Test body for pic',
            pic=cls.default_picture
        )
        cls.pic.save()
        cls.pic.tags.add('mcqueen', 'car')

    @classmethod
    def close_file_and_delete_pic(cls):
        cls.img.close()
        cls.pic.delete()


class TestPicForm(SimpleTestCase):
    def setUp(self):
        self.response = self.client.get(reverse('vcars:post_pic'))

    def test_pic_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PicForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_validation_form(self):
        img = open(BASE_DIR / 'media/default.png', 'rb')
        data = {'tags': ['1', '2', 'asfsaf'], 'name': 'luigi',
                'body': 'blabla'}
        invalid_data = {'tags': '', 'name': '', 'body': ''}
        files = {'pic': SimpleUploadedFile(
            name='default.png',
            content=img.read(),
            content_type='image/png'
        )}
        valid_form = PicForm(
            data=data, files=files)
        invalid_form = PicForm(data=invalid_data, files=files)
        img.close()
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())


class TestModelPic(PicCreationMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().create_pic()

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

    def test_get_and_delete_tags(self):
        tags_list = [name[0] for name in self.pic.tags.values_list('name')]
        self.assertEqual(tags_list, ['mcqueen', 'car'])
        self.pic.tags.remove('car')
        self.assertEqual(self.pic.tags.count(), 1)

    @classmethod
    def setDownClass(cls):
        super().close_file_and_delete_pic()


class TestVcarsUrls(PicCreationMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().create_pic()

    def test_index_page(self):
        url_path = reverse('vcars:index')
        request = self.client.get(url_path)
        resolver = resolve(url_path)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(resolver.func.view_class, PictureListView)

    def test_retrieve_page_url(self):
        url_path = reverse('vcars:pic_detail', args=[self.pic.slug])
        response = self.client.get(url_path)
        resolver = resolve(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolver.func.view_class, PicDetailView)

    def test_add_pic_url(self):
        url_path = reverse('vcars:post_pic')
        resolver = resolve(url_path)
        with open(BASE_DIR / 'media/default.png', 'rb') as img:
            response = self.client.post(url_path, {
                'name': 'New Car Pic',
                'body': 'Test body for new pic',
                'pic': img,
                'tags': ['mcqueen', 'car'],
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolver.func.view_class, CreatePic)

    def test_add_comment_url(self):
        url_path = reverse('vcars:pic_detail', args=[self.pic.slug])
        response = self.client.post(url_path, data={'name': 'abobus', 'body': 'comment'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'abobus')
        self.assertContains(response, 'comment')
        self.assertTrue(Pic.objects.get(pk=2).comments.count())

    def test_filter_by_tags_url(self):
        url_path = reverse('vcars:tagged_index', args=['mcqueen'])
        resolver = resolve(url_path)
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolver.func.view_class, PictureListView)
        url_path2 = reverse('vcars:tagged_index', args=['mcquklklkeen'])
        response2 = self.client.get(url_path2)
        self.assertEqual(response2.status_code, 404)

    @classmethod
    def setDownClass(cls):
        super().close_file_and_delete_pic()
