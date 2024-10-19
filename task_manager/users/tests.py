from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.
class UserTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls._get = reverse('users')
        cls._create = reverse('create_user')
        # cls._update = reverse('update_user')
        # cls._delete = reverse('delete_user')
    
        cls.user1 = User.objects.create(
            first_name='Foo',
            last_name='Buzz1',
            username='FooBuzz1',
            email='FooBuzz1@gl.ru',
            password='123qwerty'
        )
        cls.user2 = User.objects.create(
            first_name='Foo',
            last_name='Buzz2',
            username='FooBuzz2',
            email='FooBuzz2@gl.ru',
            password='123qwerty'
        )

    def test_get(self):
        response = self.client.get(self._get)
        self.assertEqual(200, response.status_code)

    def test_create_user(self):
        self.assertEqual(2, User.objects.all().count())
        print(self._create)
        response = self.client.post(
            self._create, {
                'first_name': 'Test',
                'last_name': 'Test',
                'username': 'Test',
                'password1': 'Test123pass',
                'password2': 'Test123pass'
            }
        )
        print(response)
        self.assertEqual(3, User.objects.all().count())

        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "users/create.html")
        self.assertRedirects(response, reverse('login'))



