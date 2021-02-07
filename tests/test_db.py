import unittest
from unittest.mock import MagicMock

from wmo.checker import CheckResult
from wmo.db import Writer


class TestWriter(unittest.TestCase):
    def test_calls_cursor_execute(self):
        cursor = MagicMock()
        some_result = CheckResult(
            url="https://example.com",
            status_code=200,
            response_time=0.123,
            pattern=None,
            matches=[],
        )

        writer = Writer("some_db_uri")
        writer.write_cursor(cursor, "some_table", some_result)

        cursor.execute.assert_called_once_with(
            (
                "INSERT INTO %s (url, status_code, response_time, pattern, matches) "
                "VALUES (%s, %s, %s, %s, %s)"
            ),
            "some_table",
            "https://example.com",
            200,
            0.123,
            None,
            "[]",
        )
