import json
import logging
from typing import Any

import psycopg2  # type: ignore
from psycopg2.sql import SQL, Identifier  # type: ignore

from .checker import CheckResult

logger = logging.getLogger(__name__)


class Writer:
    """ Writes a `CheckResult` into a specified PostgreSQL table """

    def __init__(self, uri: str):
        self._uri = uri

    def write(self, table: str, result: CheckResult) -> None:
        try:
            with psycopg2.connect(self._uri) as connection:
                with connection.cursor() as cursor:
                    self.write_cursor(cursor, table, result)
        except psycopg2.Error:
            logger.exception("Couldn't write into the database")

    def write_cursor(self, cursor: Any, table: str, result: CheckResult) -> None:
        logger.info("Writing %s to table %s", result, table)
        cursor.execute(
            SQL(
                "INSERT INTO {} (url, status_code, response_time, pattern, matches) "
                "VALUES (%s, %s, %s, %s, %s)"
            ).format(Identifier(table)),
            (
                result.url,
                result.status_code,
                result.response_time,
                result.pattern,
                json.dumps(result.matches),
            ),
        )
