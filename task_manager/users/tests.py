from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.url = reverse('create_user')
    
        self.user1 = User.objects.create(
            first_name='Foo',
            last_name='Buzz1',
            username='FooBuzz1',
            email='FooBuzz1@gl.ru',
            password='123qaz'
        )
        self.user2 = User.objects.create(
            first_name='Foo',
            last_name='Buzz2',
            username='FooBuzz2',
            email='FooBuzz2@gl.ru',
            password='123qaz'
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

