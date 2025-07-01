from django.test import TestCase, Client
from django.urls import reverse
from .models import Users
from django.contrib.messages import get_messages
from .models import Statuses
from .forms import StatusForm


class StatusesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Users.objects.create_user(
            username='user1', password='password123'
        )
        self.user2 = Users.objects.create_user(
            username='user2', password='password123'
        )
        self.status1 = Statuses.objects.create(
            name='Status 1', created_by=self.user1
        )
        self.status2 = Statuses.objects.create(
            name='Status 2', created_by=self.user2
        )

        self.statuses_url = reverse('statuses')
        self.create_url = reverse('create_status')
        self.update_url = reverse('update_status', args=[self.status1.id])
        self.delete_url = reverse('delete_status', args=[self.status1.id])

    def test_statuses_view_GET(self):
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/statuses_list.html')
        self.assertContains(response, 'Status 1')
        self.assertContains(response, 'Status 2')

    def test_create_status_GET_authenticated(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create_status.html')
        self.assertIsInstance(response.context['form'], StatusForm)

    def test_create_status_GET_unauthenticated(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.create_url}')

    def test_create_status_POST_valid(self):
        self.client.login(username='user1', password='password123')
        data = {'name': 'New Status'}
        response = self.client.post(self.create_url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно создан')
        self.assertEqual(Statuses.objects.count(), 3)
        new_status = Statuses.objects.latest('id')
        self.assertEqual(new_status.created_by, self.user1)
        self.assertRedirects(response, self.statuses_url)

    def test_update_status_GET_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update_status.html')

    def test_update_status_GET_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.update_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Вы не можете редактировать чужой статус.')
        self.assertRedirects(response, self.statuses_url)

    def test_update_status_GET_unauthenticated(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_status_POST_valid(self):
        self.client.login(username='user1', password='password123')
        data = {'name': 'Updated Status'}
        response = self.client.post(self.update_url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно изменён')
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'Updated Status')
        self.assertRedirects(response, self.statuses_url)

    def test_delete_status_GET_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete_status.html')

    def test_delete_status_GET_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.delete_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Вы не можете удалить чужой статус.')
        self.assertRedirects(response, self.statuses_url)

    def test_delete_status_GET_unauthenticated(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/statuses/'))

    def test_delete_status_POST_success(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.delete_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно удалён')
        self.assertEqual(Statuses.objects.count(), 1)
        self.assertRedirects(response, self.statuses_url)
