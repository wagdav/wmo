import unittest
from unittest.mock import ANY, MagicMock

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
            ANY,  # placeholder for the query
            (
                "https://example.com",
                200,
                0.123,
                None,
                "[]",
            ),
        )
