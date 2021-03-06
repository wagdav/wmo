import unittest
from datetime import timedelta
from unittest.mock import create_autospec

import requests

from wmo.checker import Checker


class TestChecker(unittest.TestCase):
    def setUp(self):
        self.session = create_autospec(requests.Session, spec_set=True)

    def test_happy_path(self):
        url = "https://example.com"
        http_response = requests.Response()
        http_response.status_code = 200
        http_response.elapsed = timedelta(milliseconds=123)

        self.session.get.return_value = http_response

        result = Checker(timeout=1, session=self.session).check_site(url)

        self.session.get.assert_called_once_with(url, timeout=1)
        self.assertEqual(result.status_code, http_response.status_code)
        self.assertGreater(result.response_time, 0)
        self.assertEqual(result.pattern, None)

    def test_returns_default_values_when_request_throws(self):
        url = "https://example.com"

        self.session.get.side_effect = requests.ConnectionError("boom")

        result = Checker(timeout=1, session=self.session).check_site(url)

        self.assertEqual(result.status_code, 0)
        self.assertEqual(result.response_time, 0)

    def test_matches_pattern(self):
        http_response = requests.Response()
        http_response._content = b"hello alice,hello bob"
        self.session.get.return_value = http_response

        somePattern = "hello ([^,]*)"

        result = Checker(
            timeout=1, pattern=somePattern, session=self.session
        ).check_site("http://example.com")

        self.assertEqual(result.pattern, somePattern)
        self.assertEqual(result.matches, ["alice", "bob"])
