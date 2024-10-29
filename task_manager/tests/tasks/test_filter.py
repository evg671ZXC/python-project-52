from task_manager.utils.filters import TaskFilter
from task_manager.tasks.models import Task
from .setup import TaskSettings


class TaskFilterTestCase(TaskSettings):
    def test_filter_by_executor(self):
        filter = TaskFilter(data={'executor': self.user.id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 2)
        self.assertEqual(filtered_tasks[0].name, 'New Task1')
        self.assertEqual(filtered_tasks[1].name, 'New Task3')

    def test_filter_by_label(self):
        filter = TaskFilter(data={
            'label': self.task.labels.first().id
        }, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 2)
        self.assertEqual(filtered_tasks[0].name, 'New Task1')
        self.assertEqual(filtered_tasks[1].name, 'New Task2')

    def test_filter_by_status(self):
        filter = TaskFilter(data={'status': self.status.id}, queryset=Task.objects.all())
        filtered_tasks = list(filter.qs)
        self.assertEqual(len(filtered_tasks), 1)

    def test_filter_self_tasks(self):
        response = self.client.get(self.urls['list'], {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Task1')
        self.assertNotContains(response, 'New Task3')
