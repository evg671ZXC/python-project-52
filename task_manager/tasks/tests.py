from django.test import TestCase, Client
from django.urls import reverse
from ..tasks.models import Task
from django.contrib.auth import get_user_model
from ..statuses.models import Status
from ..labels.models import Label
from ..utils.filters import TaskFilter

# Create your tests here.
class TaskCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password123test')
        self.client.force_login(self.user)
        self.status = Status.objects.create(name='New')
        self.label = Label.objects.create(name='Test Label')
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            status=self.status,
            author=self.user,
            performer=self.user
        )
        self.task.labels.add(self.label)

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        response = self.client.get(reverse('task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_create_task_view(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')


        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'New Test Task',
                'description': 'Another test task',
                'status': self.status.id,
                'performer': self.user.id,
                'labels': [self.label.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='New Test Task').exists())

    def test_update_task_view(self):
        response = self.client.get(reverse('update_task', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            reverse('update_task', kwargs={'pk': self.task.pk}),
            {
                'name': 'Updated Test Task',
                'description': 'This task was updated',
                'status': self.status.id,
                'performer': self.user.id,
                'labels': [self.label.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.name, 'Updated Test Task')
        self.assertEqual(updated_task.description, 'This task was updated')

    def test_delete_task_view(self):
        response = self.client.post(
            reverse('delete_task', kwargs={'pk': self.task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


class TaskFilterTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = get_user_model().objects.create_user(username='filteruser1', password='filterpass')
        self.user2 = get_user_model().objects.create_user(username='filteruser2', password='filterpass')

        self.client.login(username='filteruser1', password='filterpass')

        self.status = Status.objects.create(name='test status')

        self.task1 = Task.objects.create(
            name='task 1',
            description="description 1",
            status=self.status,
            author=self.user1,
            performer=self.user1
        )
        self.task1.labels.add(Label.objects.create(name='label 1'))
    
        self.task2 = Task.objects.create(
            name='task 2',
            description="description 2",
            status=self.status,
            author=self.user2,
            performer=self.user2
        )
        self.task2.labels.add(Label.objects.create(name='label 2'))

    def test_filter_by_performer(self):
        filter = TaskFilter(data={'performer': self.user1.id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0].name, 'task 1')

    def test_filter_by_label(self):
        filter = TaskFilter(data={'label': self.task1.labels.first().id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0].name, 'task 1')

    def test_filter_by_status(self):
        filter = TaskFilter(data={'status': self.status.id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 2)

    def test_filter_self_tasks(self):
        response = self.client.get(reverse('tasks'), {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'task 1')
        self.assertNotContains(response, 'task 2')
