from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses


class CrudLabelsTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Users.objects.create_user(username='user1', password='12345')
        self.user2 = Users.objects.create_user(username='user2', password='12345')
        self.status1 = Statuses.objects.create(name='In Progress', created_by=self.user1)
        self.label1 = Labels.objects.create(name='Label1')
        self.label2 = Labels.objects.create(name='Label2')
        self.task1 = Tasks.objects.create(name='Task1',
                                          description='Desc1',
                                          author=self.user1,
                                          status=self.status1,
                                          assigned_to=self.user1,
                                          )
        self.task1.labels.add(self.label1)
        self.task2 = Tasks.objects.create(name='Task2',
                                          description='Desc2',
                                          author=self.user2,
                                          status=self.status1,
                                          assigned_to=self.user2)
        self.client.login(username='user1', password='12345')

    def test_list_labels(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')

    def test_create_labels(self):
        self.assertEqual(Labels.objects.count(), 2)
        response = self.client.post(reverse('label_create'), {'name': 'NewLAbel'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Labels.objects.count(), 3)

    def test_update_labels(self):
        url_path = reverse('label_update', kwargs={'pk': self.label1.pk})
        response = self.client.post(url_path, {'name': "UpdateLabel"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Labels.objects.get(pk=self.label1.pk).name, 'UpdateLabel')

    def test_delete_own_labels(self):
        url_path = reverse('label_delete', kwargs={'pk': self.label2.pk})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(Labels.objects.count(), 1)

    def test_delete_linked_labels(self):
        url_path = reverse('label_delete', kwargs={'pk': self.label1.pk})
        response = self.client.post(url_path)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Нельзя удалить метку, связанную с задачами')

    def tearDown(self):
        self.client.logout()
        Tasks.objects.all().delete()
        Labels.objects.all().delete()
        Users.objects.all().delete()
