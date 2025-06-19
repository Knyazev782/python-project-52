from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses

class CrudTasksTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Users.objects.create_user(username='user1', password='12345')
        self.user2 = Users.objects.create_user(username='user2', password='12345')
        self.status1 = Statuses.objects.create(name='In Progress', created_by=self.user1)

        self.task1 = Tasks.objects.create(name='Task1',
                                        description='Desc1',
                                        author=self.user1,
                                        status=self.status1,
                                        assigned_to=self.user1)
        self.task2 = Tasks.objects.create(name='Task2',
                                        description='Desc2',
                                        author=self.user2,
                                        status=self.status1,
                                        assigned_to=self.user2)

        self.client.login(username='user1', password='12345')

    def test_list_tasks(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_list.html')

    def test_create_task(self):
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Desc',
            'assigned_to': str(self.user1.id),
            'status': str(self.status1.id),
            'author': str(self.user1.id)
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tasks.objects.count(), 3)

    def test_update_own_task(self):
        url_path = reverse('task_update', kwargs={'pk': self.task1.pk})
        response = self.client.post(url_path, {
            'name': 'Updated Task',
            'description': 'Updated Desc',
            'assigned_to': str(self.user1.id),
            'status': str(self.status1.id),
            'author': str(self.user1.id)
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tasks.objects.get(pk=self.task1.pk).name, 'Updated Task')

    def test_update_another_task(self):
        url_path = reverse('task_update', kwargs={'pk': self.task2.pk})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы не можете изменять эту задачу!")

    def test_delete_own_task(self):
        url_path = reverse('task_delete', kwargs={'pk': self.task1.pk})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(Tasks.objects.count(), 1)

    def test_delete_another_task(self):
        url_path = reverse('task_delete', kwargs={'pk': self.task2.pk})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы не можете удалять эту задачу!")

    def tearDown(self):
        self.client.logout()
        Tasks.objects.all().delete()
        Statuses.objects.all().delete()
        Users.objects.all().delete()