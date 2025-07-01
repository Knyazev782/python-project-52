from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from .models import Tasks


class TasksViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Users.objects.create_user(
            username='user1',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.user2 = Users.objects.create_user(
            username='user2',
            password='password123',
            first_name='Jane',
            last_name='Smith'
        )

        self.status1 = Statuses.objects.create(name='Status 1', created_by=self.user1)
        self.status2 = Statuses.objects.create(name='Status 2', created_by=self.user2)

        self.label1 = Labels.objects.create(name='Label 1', created_by=self.user1)
        self.label2 = Labels.objects.create(name='Label 2', created_by=self.user2)

        self.task = Tasks.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status1,
            author=self.user1,
            assigned_to=self.user2
        )
        self.task.labels.add(self.label1)

        self.tasks_url = reverse('tasks')
        self.create_url = reverse('task_create')
        self.detail_url = reverse('task_detail', args=[self.task.id])
        self.update_url = reverse('task_update', args=[self.task.id])
        self.delete_url = reverse('task_delete', args=[self.task.id])

    def test_tasks_view(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_list.html')
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'Test Task')

    def test_create_task_view_get(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_create.html')

    def test_create_task_view_post(self):
        self.client.login(username='user1', password='password123')
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status1.id,
            'author': self.user1.id,
            'assigned_to': self.user2.id,
            'labels': [self.label1.id]
        }
        response = self.client.post(self.create_url, data, follow=True)

        new_task = Tasks.objects.filter(name='New Task').first()
        self.assertIsNotNone(new_task)

        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

    def test_update_task_view_get(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_update.html')

    def test_update_task_view_post(self):
        self.client.login(username='user1', password='password123')
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status2.id,
            'author': self.user1.id,
            'assigned_to': self.user1.id,
            'labels': [self.label2.id]
        }
        response = self.client.post(self.update_url, data, follow=True)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

    def test_delete_task_view_get(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_delete.html')

    def test_delete_task_view_post(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.delete_url, follow=True)

        self.assertFalse(Tasks.objects.filter(id=self.task.id).exists())

        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

    def test_permission_checks(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.update_url, follow=True)
        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не можете редактировать чужую задачу.')

        response = self.client.post(self.delete_url, follow=True)
        self.assertRedirects(response, self.tasks_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не можете удалять чужую задачу.')
