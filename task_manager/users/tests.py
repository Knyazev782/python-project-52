from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Nickname',
                                             password='Password123')

        self.other_user = User.objects.create_user(username="OtherUser",
                                                   password="Password123")

    @staticmethod
    def get_form_data(**kwargs):
        valid_data = {
                      'username': 'NewUser',
                      'first_name': 'name',
                      'last_name': 'last_name',
                      'password1': 'Password123',
                      'password2': 'Password123'
                     }
        valid_data.update(kwargs)
        return valid_data

    def test_create_user(self):
        register = reverse('create_users')
        request = self.client.post(register, self.get_form_data(username="NewUser1"),
                                        follow=True)
        self.assertRedirects(request, '/login/', status_code=302)
        self.assertTrue(User.objects.filter(username="NewUser1").exists())

    def test_create_user_invalid(self):
        register = reverse('create_users')
        request = self.client.post(register, self.get_form_data(password2="Pass111"))
        self.assertEqual(request.status_code, 200)
        self.assertFalse(User.objects.filter(username="NewUser").exists())

    def test_update_user_if_logged(self):
        self.client.force_login(self.user)
        url = reverse('update_users', args=[self.user.id])
        request = self.client.post(url, self.get_form_data(first_name="NewName"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.first_name == "NewName")
        self.assertRedirects(request, '/users/', status_code=302)
        self.assertTrue(User.objects.filter(first_name="NewName").exists())

    def test_update_user_if_not_logged(self):
        self.client.force_login(self.other_user)
        self.user.first_name = "OldName"
        self.user.save()
        url = reverse('update_users', args=[self.user.id])
        request = self.client.post(url, self.get_form_data(first_name='name'))
        self.assertRedirects(request, '/users/', status_code=302)
        self.assertTrue(User.objects.filter(first_name='OldName').exists())

    def test_delete_user_if_logged(self):
        self.client.force_login(self.user)
        url =reverse('delete_users', args=[self.user.id])
        request = self.client.post(url, self.get_form_data(first_name='name'))
        self.assertRedirects(request, '/users/', status_code=302)
        self.assertFalse(User.objects.filter(username="Nickname").exists())

    def test_delete_user_if_not_logged(self):
        self.client.force_login(self.other_user)
        url = reverse('delete_users', args=[self.user.id])
        request = self.client.post(url, self.get_form_data(first_name='name'))
        self.assertTrue(User.objects.filter(username="Nickname").exists())
        self.assertRedirects(request, '/users/', status_code=302)
        self.assertTrue(User.objects.filter(username="Nickname").exists())

    def test_login_required(self):
        request = self.client.get('/users/')
        self.assertEqual(request.status_code, 200)

    def test_view_users(self):
        request = self.client.get('/users/')
        self.assertEqual(request.status_code, 200)

    def test_login(self):
        login_url = reverse('login')
        request = self.client.post(login_url, {
            'username': 'Nickname',
            'password': 'Password123'},
            follow=True)
        self.assertRedirects(request, '/', status_code=302)

    def test_logout(self):
        self.client.force_login(self.user)
        logout_url = reverse('logout')
        request = self.client.post(logout_url, follow=True)
        self.assertRedirects(request, '/', status_code=302)
