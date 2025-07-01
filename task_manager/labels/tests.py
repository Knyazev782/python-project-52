from django.test import TestCase, Client
from django.urls import reverse
from .models import Users
from django.contrib.messages import get_messages
from .models import Labels
from .forms import LabelForm


class LabelsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Users.objects.create_user(
            username='user1', password='password123'
        )
        self.user2 = Users.objects.create_user(
            username='user2', password='password123'
        )
        self.label1 = Labels.objects.create(
            name='Label 1', created_by=self.user1
        )
        self.label2 = Labels.objects.create(
            name='Label 2', created_by=self.user2
        )

        self.labels_url = reverse('labels')
        self.create_url = reverse('label_create')
        self.update_url = reverse('label_update', args=[self.label1.id])
        self.delete_url = reverse('label_delete', args=[self.label1.id])

    def test_labels_view_GET(self):
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertContains(response, 'Label 1')
        self.assertContains(response, 'Label 2')

    def test_create_label_GET_authenticated(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_create.html')
        self.assertIsInstance(response.context['form'], LabelForm)

    def test_create_label_GET_unauthenticated(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.create_url}')

    def test_create_label_POST_valid(self):
        self.client.login(username='user1', password='password123')
        data = {'name': 'New Label'}
        response = self.client.post(self.create_url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно создана')
        self.assertEqual(Labels.objects.count(), 3)
        self.assertEqual(Labels.objects.last().created_by, self.user1)
        self.assertRedirects(response, self.labels_url)

    def test_update_label_GET_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_update.html')

    def test_update_label_GET_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.update_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Вы не можете редактировать чужую метку.')
        self.assertRedirects(response, self.labels_url)

    def test_update_label_POST_valid(self):
        self.client.login(username='user1', password='password123')
        data = {'name': 'Updated Label'}
        response = self.client.post(self.update_url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно изменена')
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, 'Updated Label')
        self.assertRedirects(response, self.labels_url)

    def test_delete_label_GET_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_delete.html')

    def test_delete_label_GET_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.delete_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Вы не можете удалить чужую метку.')
        self.assertRedirects(response, self.labels_url)

    def test_delete_label_POST_success(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.delete_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')
        self.assertEqual(Labels.objects.count(), 1)
        self.assertRedirects(response, self.labels_url)
