from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Label


# Create your tests here.
class TestLabelsView(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='test123pass'
        )
        self.client.force_login(self.user)
        self.label = Label.objects.create(name='test view')

        self.labels_url = reverse('labels')
        self.create_label_url = reverse('create_label')
        self.update_label_url = lambda pk: reverse('update_label', args=[pk])
        self.delete_label_url = lambda pk: reverse('delete_label', args=[pk])

    def test_label_index_view(self):
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test view')

    def test_create_label_view(self):
        response = self.client.post(
            self.create_label_url,
            {'name': 'New Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Label created successfully')
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_update_label_view(self):
        response = self.client.post(
            self.update_label_url(self.label.pk),
            {'name': 'Updated Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Label successfully changed')
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_delete_label_view(self):
        response = self.client.post(self.delete_label_url(self.label.pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
