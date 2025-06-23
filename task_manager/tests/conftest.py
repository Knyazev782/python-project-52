import pytest
from django.core.management import call_command
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """Создает и применяет миграции к тестовой базе перед запуском тестов."""
    logger.debug("Starting database setup for tests...")
    with django_db_blocker.unblock():
        logger.debug("Applying migrations...")
        call_command("migrate", "--noinput")
        logger.debug("Migrations applied successfully.")
    logger.debug("Database setup completed.")