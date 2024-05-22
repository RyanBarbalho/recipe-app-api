"""
Test custom Django management commands.
"""
from unittest.mock import patch #mock the behavior of database connection # noqa

from psycopg2 import OperationalError as Psycopg2Error #psycopg2 is the database driver for PostgreSQL, example of error when database is not available # noqa

from django.core.management import call_command #allows to call management commands from the code # noqa
from django.db.utils import OperationalError# noqa
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test commands
    """
    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for db when db is available
        """
        patched_check.return_value = True

        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')#object that will return a none value every time it is called # noqa
    def test_wait_for_db_delay(self, pathced_sleep, patched_check):
        """
        Test waiting for db when getting operational error
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]  ## 2 times psycopg2 error, 3 times operational error, then True # noqa

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
