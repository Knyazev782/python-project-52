import pytest
from django.test import Client

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='testuser',
        password='testpassword',
        first_name='Test',
        last_name='User',
        email='test@example.com'
    )

@pytest.fixture
def client_logged(user):
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client
