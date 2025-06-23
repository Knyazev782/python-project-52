import pytest
from django.core.management import call_command
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_blocker):
    logger.debug("Attempting to set up test database...")
    try:
        with django_db_blocker.unblock():
            logger.debug("Applying migrations for test environment...")
            call_command("migrate", "--noinput")
            logger.debug("Migrations applied successfully.")
    except Exception as e:
        logger.error(f"Failed to apply migrations: {e}")
        raise
    logger.debug("Test database setup completed.")