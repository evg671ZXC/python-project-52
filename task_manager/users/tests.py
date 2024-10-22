from django.test import TestCase, Client
from django.urls import reverse
from .models import User

# Create your tests here.
class UserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
    
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123'
        )

        self.index = '/'
        self.users_url = reverse('users')
        self.create_user_url = reverse('create_user')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.update_user_url = lambda pk: reverse('update_user', args=[pk])
        self.delete_user_url = lambda pk: reverse('delete_user', args=[pk])

    def _login(self, username, password):
        response = self.client.post(self.login_url, {'username': username, 'password': password})
        self.assertRedirects(response, self.index, 302)
    
    def test_logout(self):
        self._login(self.user1.username, 'testpassword123')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.index, 302)

    def test_get_users(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["users"]), 2)

    def test_create_user(self):
        response = self.client.get(self.create_user_url)
        self.assertTemplateUsed(response, template_name="users/create.html")

        new_user_data = {
                'username': 'testuser3',
                'email': 'test2@example.com',
                'password1': 'testpassword123',
                'password2': 'testpassword123'
            }

        response = self.client.post(self.create_user_url, new_user_data)
        self.assertEqual(User.objects.last().username, new_user_data['username'])
        self.assertRedirects(response, self.login_url, 302)


    def test_update_user(self):
        self._login(self.user1.username, 'testpassword123')

        update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        response = self.client.post(self.update_user_url(self.user1.pk), update_data)
        self.assertRedirects(response, self.login_url, 302)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')


    def test_delete_user(self):
        # Проверка неавторизованного доступа
        response = self.client.get(self.delete_user_url(self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_url)

        # Удаление от другого аккаунта
        self._login(self.user2.username, 'testpassword123')

        response = self.client.post(self.delete_user_url(self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_url, 302)

        # Авторизация и удаление аккаунта
        self._login(self.user1.username, 'testpassword123')

        initial_count = User.objects.count()
        response = self.client.post(self.delete_user_url(self.user1.pk))
        final_count = User.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_url)
        self.assertEqual(initial_count - 1, final_count)
        with self.assertRaisesMessage(User.DoesNotExist,
                                      'does not exist'):
            User.objects.get(username='testuser1')
