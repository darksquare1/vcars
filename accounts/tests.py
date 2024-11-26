from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile


class UserCreationMixin:
    @classmethod
    def create_user(cls):
        cls.username = 'testuser'
        cls.password = 'fsalfsazx0521@'
        cls.first_name = 'lightning'
        cls.last_name = 'mcqueen'
        cls.email = 'asdsad@asdasd.com'
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)


class TestSignup(TestCase):
    def test_signup_page(self):
        url_path = reverse('signup')
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'passwordpassword000111591',
            'password2': 'passwordpassword000111591',
        }
        response2 = self.client.post(url_path, data=data)
        self.assertRedirects(response2, reverse('vcars:index'))
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user.profile)
        self.assertTemplateUsed(response, 'registration/signup.html')


class TestLogin(UserCreationMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().create_user()

    def test_login_page(self):
        url_path = reverse('login')
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(url_path, data={'username': self.username, 'password': self.password})
        self.assertRedirects(response2, reverse('vcars:index'))
        self.assertTemplateUsed(response, 'registration/login.html')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()


class TestProfile(UserCreationMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().create_user()
        cls.profile = Profile.objects.create(user=cls.user)

    def test_profile_page(self):
        url_path = reverse('profile', args=[self.user.profile.slug])
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        self.client.login(username=self.username, password=self.password)
        response2 = self.client.post(reverse('profile_edit'),
                                     data={'first_name': 'Bob', 'last_name': 'Bib', 'username': self.username,
                                           'email': self.email})
        self.assertRedirects(response2, url_path)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Bob')
        self.assertEqual(self.user.last_name, 'Bib')
        self.assertTemplateUsed(response, 'registration/profile.html')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()


class VerifyViewTestCase(UserCreationMixin, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().create_user()
        cls.profile = Profile.objects.create(user=cls.user)

    def test_verify_user(self):
        url_path = reverse('verify', args=[self.profile.verification_uuid])
        response = self.client.get(url_path)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_verified)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/verify.html')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
