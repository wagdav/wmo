import logging
from typing import List, Optional
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    url: str
    status_code: int
    response_time: float
    pattern: str
    matches: List[str]


class Checker:
    def __init__(self, timeout: float, session: Optional[requests.Session] = None):
        self._session = session or requests.Session()
        self._timeout = timeout

    def check_site(self, url) -> CheckResult:
        try:
            response = self._session.get(url, timeout=self._timeout)
            return CheckResult(
                url=url,
                status_code=response.status_code,
                response_time=response.elapsed.total_seconds(),
                pattern="",
                matches=[],
            )
        except requests.RequestException:
            logger.info("Couldn't reach the website %s", url)
            return CheckResult(
                url=url,
                status_code=0,
                response_time=0,
                pattern="",
                matches=[],
            )

    def check_sites(self, urls: List[str]) -> List[CheckResult]:
        return [self.check_site(url) for url in urls]
