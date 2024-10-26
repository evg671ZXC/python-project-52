from task_manager.labels.models import Label
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    fixtures = ['labels_db.json', 'users_db.json']

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.get(username='test_user1')
        self.client.force_login(self.user)

        self.label = Label.objects.get(name='New label1')

        self.urls = {
            'list': reverse('labels'),
            'create': reverse('create_label'),
            'update': lambda pk: reverse('update_label', args=[pk]),
            'delete': lambda pk: reverse('delete_label', args=[pk]),
        }

    def test_label_index_view(self):
        response = self.client.get(self.urls['list'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New label1')
    
    def test_create_label_view(self):
        response = self.client.post(
            self.urls['create'],
            {'name': 'New Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Label created successfully')
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_update_label_view(self):
        response = self.client.post(
            self.urls['update'](self.label.pk),
            {'name': 'Updated Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Label successfully changed')
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_delete_label_view(self):
        response = self.client.post(self.urls['delete'](self.label.pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
