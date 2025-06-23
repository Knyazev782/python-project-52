import os
import pytest
from django.core.management import call_command
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def django_db_setup():
    logger.debug("Setting up test database...")
    db_path = "test_db.sqlite3"
    if os.path.exists(db_path):
        logger.debug("Removing existing test database...")
        os.remove(db_path)
    # Явное создание файла перед миграциями
    with open(db_path, 'a'):
        pass  # Создаем пустой файл
    logger.debug(f"Database file created at: {os.path.abspath(db_path)}")
    call_command("migrate", "--noinput")
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        logger.error("Test database file was not populated!")
        raise Exception("Failed to populate test_db.sqlite3")
    logger.debug("Migrations applied successfully.")