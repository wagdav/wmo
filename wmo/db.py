from typing import Any
import json
import logging

import psycopg2  # type: ignore

from .checker import CheckResult

logger = logging.getLogger(__name__)


class Writer:
    """ Writes a `CheckResult` into a specified PostgreSQL table """

    def __init__(self, dbname: str, user: str, password: str):
        self._dbname = dbname
        self._user = user
        self._password = user

    def write(self, table: str, result: CheckResult) -> None:
        try:
            with psycopg2.connect(
                dbname=self._dbname, user=self._user, password=self._password
            ) as connection:
                with connection.cursor() as cursor:
                    self.write_cursor(cursor, table, result)
        except psycopg2.Error:
            logger.exception("Couldn't write into the database")

    def write_cursor(self, cursor: Any, table: str, result: CheckResult) -> None:
        cursor.execute(
            (
                "INSERT INTO %s (url, status_code, response_time, pattern, matches) "
                "VALUES (%s, %s, %s, %s, %s)"
            ),
            table,
            result.url,
            result.status_code,
            result.response_time,
            result.pattern,
            json.dumps(result.matches),
        )
