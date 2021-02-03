import unittest

import requests_mock

from wmo.checker import Checker


class TestChecker(unittest.TestCase):
    def test_it_works(self):
        url = "https://example.com"

        checker = Checker()

        with requests_mock.Mocker(session=checker._session) as session_mock:
            session_mock.get(url, text='session')

            result = checker.check_site(url)

            self.assertEqual(result.status_code, 200)
