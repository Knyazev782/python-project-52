import pytest
from django.core.management import call_command

@pytest.fixture(autouse=True)
def apply_migrations():
    call_command('migrate', '--noinput')