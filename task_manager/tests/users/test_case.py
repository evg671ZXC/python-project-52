from task_manager.users.models import User
from django.test import TestCase, Client
from django.urls import reverse


class UserTestCase(TestCase):
    fixtures = ['users_db.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(username='test_user1')
        self.user2 = User.objects.get(username='test_user2')

        self.urls = {
            'index': '/',
            'login': reverse('login'),
            'logout': reverse('logout'),
            'list': reverse('users'),
            'create': reverse('create_user'),
            'update': lambda pk: reverse('update_user', args=[pk]),
            'delete': lambda pk: reverse('delete_user', args=[pk]),
        }
    
    def _login(self, username, password):
        response = self.client.post(self.urls['login'], {'username': username, 'password': password})
        self.assertRedirects(response, self.urls['index'], 302)
    
    def test_logout(self):
        self._login(self.user1.username, 'password123pass')
        response = self.client.post(self.urls['logout'])
        self.assertRedirects(response, self.urls['index'], 302)
    
    def test_get_users(self):
        response = self.client.get(self.urls['list'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["users"]), 2)
    
    def test_create_user(self):
        response = self.client.get(self.urls['create'])
        self.assertTemplateUsed(response, template_name="users/create.html")

        new_user_data = {
            'username': 'testuser3',
            'email': 'test2@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }

        response = self.client.post(self.urls['create'], new_user_data)
        self.assertEqual(User.objects.last().username, new_user_data['username'])
        self.assertRedirects(response, self.urls['login'], 302)
    
    def test_update_user(self):
        self._login(self.user1.username, 'password123pass')

        update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        response = self.client.post(self.urls['update'](self.user1.pk), update_data)
        self.assertRedirects(response, self.urls['login'], 302)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')

    def test_delete_user(self):
        # Проверка неавторизованного доступа
        response = self.client.get(self.urls['delete'](self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls['list'])

        # Удаление от другого аккаунта
        self._login(self.user2.username, 'password123pass')

        response = self.client.post(self.urls['delete'](self.user1.pk))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls['list'])

        # Авторизация и удаление аккаунта
        self._login(self.user1.username, 'password123pass')

        initial_count = User.objects.count()
        response = self.client.post(self.urls['delete'](self.user1.pk))
        final_count = User.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls['list'])
        self.assertEqual(initial_count - 1, final_count)
        with self.assertRaisesMessage(User.DoesNotExist,
                                      'does not exist'):
            User.objects.get(username='testuser1')