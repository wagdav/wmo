import unittest
from unittest.mock import create_autospec

from kafka import KafkaProducer

from wmo.checker import CheckResult
from wmo.messenger import Sender


class TestMessenger(unittest.TestCase):
    def test_calls_kafka_producer_send(self):
        producer = create_autospec(KafkaProducer, spec_set=True)
        msg = CheckResult(
            url="https://example.com",
            status_code=200,
            response_time=0.123,
            pattern=None,
            matches=[],
        )

        Sender("someTopic", producer).send(msg)

        producer.send.assert_called_once_with(
            "someTopic",
            (
                b'{"url": "https://example.com", "status_code": 200, '
                b'"response_time": 0.123, "pattern": null, "matches": []}'
            ),
        )
