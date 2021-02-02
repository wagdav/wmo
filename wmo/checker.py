import logging
from datetime import timedelta
from typing import List
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    url: str
    status_code: int
    response_time: timedelta
    pattern: str
    matches: List[str]


class Checker:
    def __init__(self, timeout: timedelta):
        self._session = requests.Session()
        self.timeout = timeout

    def check_site(self, url) -> CheckResult:
        try:
            self._session.get(url, timeout=self.timeout)
        except requests.RequestException:
            logger.exception("Couldn't fetch the url %s", url)

        return CheckResult(
            url=url,
            status_code=200,
            response_time=timedelta(seconds=1),
            pattern="",
            matches=[],
        )

    def check_sites(self, urls: List[str]) -> List[CheckResult]:
        return [self.check_site(url) for url in urls]
