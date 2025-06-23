import pytest
from django.core.management import call_command
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    logger.debug("Initializing test database setup...")
    try:
        with django_db_blocker.unblock():
            logger.debug("Flushing existing database...")
            call_command("flush", "--noinput", verbosity=2)
            logger.debug("Applying all migrations...")
            call_command("migrate", "--noinput", verbosity=2)
            logger.debug("Verifying database connection...")
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_users';")
            if not cursor.fetchone():
                logger.error("Table 'users_users' not found after migration!")
                raise Exception("Migration failed to create users_users table.")
            logger.debug("Table 'users_users' verified successfully.")
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise
    logger.debug("Test database setup completed.")