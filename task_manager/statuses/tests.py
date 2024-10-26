from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Status


# Create your tests here.
class StatusViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='test123pass'
        )
        self.client.force_login(self.user)

        self.status = Status.objects.create(name='Old Name')

        self.statuses_url = reverse('statuses')
        self.create_status_url = reverse('create_status')
        self.update_status_url = lambda pk: reverse('update_status', args=[pk])
        self.delete_status_url = lambda pk: reverse('delete_user', args=[pk])

    def test_status_list(self):
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        response = self.client.post(
            self.create_status_url,
            {'name': 'test status'}
        )
        self.assertRedirects(response, self.statuses_url)
        self.assertEqual(Status.objects.count(), 2)

    def test_update_status(self):
        response = self.client.get(self.update_status_url(self.status.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_form.html')

        response = self.client.post(
            self.update_status_url(self.status.pk),
            {'name': 'Updated Name'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Name')

    def test_delete_status(self):
        response = self.client.post(self.delete_status_url(self.status.pk))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 1)
