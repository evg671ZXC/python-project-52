from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class TaskSettings(TestCase):
    fixtures = ['tasks_db.json', 'labels_db.json', 'statuses_db.json', 'users_db.json']

    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.get(username='test_user1')
        self.client.force_login(self.user)

        self.status = Status.objects.get(name='New status1')
        self.label = Label.objects.get(name='New label1')
        self.task = Task.objects.get(name='New Task1')

        self.urls = {
            'list': reverse('tasks'),
            'create': reverse('create_task'),
            'detail': lambda pk: reverse('task', args=[pk]),
            'update': lambda pk: reverse('update_task', args=[pk]),
            'delete': lambda pk: reverse('delete_task', args=[pk]),
        }
