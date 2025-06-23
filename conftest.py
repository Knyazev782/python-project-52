import pytest

@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        from django.core.management import call_command
        call_command('migrate', '--noinput')