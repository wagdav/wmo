import logging
import re
from dataclasses import dataclass
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    url: str
    status_code: int
    response_time: float
    pattern: Optional[str]
    matches: List[str]


class Checker:
    def __init__(
        self,
        timeout: float,
        pattern: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        self._session = session or requests.Session()
        self._timeout = timeout
        self._pattern = pattern

    def check_site(self, url) -> CheckResult:
        p = self._compile_regexp()

        try:
            response = self._session.get(url, timeout=self._timeout)
            return CheckResult(
                url=url,
                status_code=response.status_code,
                response_time=response.elapsed.total_seconds(),
                pattern=self._pattern,
                matches=p.findall(response.text) if p else [] if self._pattern else [],
            )
        except requests.RequestException:
            logger.info("Couldn't reach the website %s", url)
            return CheckResult(
                url=url,
                status_code=0,
                response_time=0,
                pattern=self._pattern,
                matches=[],
            )

    def check_sites(self, urls: List[str]) -> List[CheckResult]:
        logging.info("Checking %d sites", len(urls))
        return [self.check_site(url) for url in urls]

    def _compile_regexp(self) -> Optional[re.Pattern]:
        if self._pattern is None:
            return None

        try:
            return re.compile(self._pattern)
        except re.error as e:
            logger.warn("Invalid regular expression: %s", e)

        return None
