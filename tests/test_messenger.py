import unittest
from dataclasses import dataclass
from unittest.mock import create_autospec

from kafka import KafkaConsumer, KafkaProducer

from wmo.checker import CheckResult
from wmo.messenger import Receiver, Sender


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

    def test_calls_kafka_consumer(self):
        @dataclass
        class ConsumerRecord:
            value: str

        consumer = create_autospec(KafkaConsumer, spec_set=True)
        consumer.__iter__.return_value = consumer
        consumer.__next__.side_effect = [
            ConsumerRecord(
                value=(
                    b'{"url": "https://example.com", "status_code": 200, '
                    b'"response_time": 0.123, "pattern": null, "matches": []}'
                )
            ),
            ConsumerRecord(value=b"{}"),  # will be ignored
        ]

        with self.assertLogs() as cm:
            self.assertEqual(
                [m for m in Receiver("someTopic", consumer)],
                [
                    CheckResult(
                        url="https://example.com",
                        status_code=200,
                        response_time=0.123,
                        pattern=None,
                        matches=[],
                    ),
                ],
            )

        consumer.subscribe.assert_called_once_with("someTopic")
        self.assertEqual(
            cm.output, ["WARNING:wmo.messenger:Ignoring the message b'{}'"]
        )
