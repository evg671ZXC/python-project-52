from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.
class UserTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.url = reverse('create_user')
    
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
        response = self.client.get(self.url)
        print(response.headers['Content-Type'])
        self.assertEqual(200, response.status_code)

    def test_create_user(self):
        self.assertEqual(2, User.objects.all().count())
        # self.client.force_login(self.user)
        response = self.client.post(
            self.url, {
                'first_name': 'Foo',
                'last_name': 'Buzz3',
                'username': 'FooBuzz3',
                'password1': '123qwerty',
                'password2': '123qwerty',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login'))
        print(response.redirect_chain)



