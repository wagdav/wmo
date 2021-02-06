import psycopg2

from .checker import CheckResult


class Writer:
    """ Writes a `CheckResult` into a specified PostgreSQL table """

    def write(self, result: CheckResult) -> None:
        pass
