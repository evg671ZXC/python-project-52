from task_manager.tasks.models import Task
from .setup import TaskSettings


class TaskTestCase(TaskSettings):
    def test_task_list_view(self):
        response = self.client.get(self.urls['list'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Task1')

    def test_task_detail_view(self):
        response = self.client.get(self.urls['detail'](self.task.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Task1')

    def test_create_task_view(self):
        response = self.client.get(self.urls['create'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_create.html')

        response = self.client.post(
            self.urls['create'],
            {
                'name': 'New Test Task',
                'description': 'Another test task',
                'status': self.status.id,
                'executor': self.user.id,
                'labels': [self.label.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls['list'])
        self.assertTrue(Task.objects.filter(name='New Test Task').exists())

    def test_update_task_view(self):
        response = self.client.get(self.urls['update'](self.task.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            self.urls['update'](self.task.pk),
            {
                'name': 'Updated Test Task',
                'description': 'This task was updated',
                'status': self.status.id,
                'executor': self.user.id,
                'labels': [self.label.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.name, 'Updated Test Task')
        self.assertEqual(updated_task.description, 'This task was updated')

    def test_delete_task_view(self):
        response = self.client.post(self.urls['delete'](self.task.pk))
        self.assertRedirects(response, self.urls['list'], 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
