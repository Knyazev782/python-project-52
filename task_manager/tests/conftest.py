import pytest
from django.core.management import call_command

@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """Создает и применяет миграции к тестовой базе перед запуском тестов."""
    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")