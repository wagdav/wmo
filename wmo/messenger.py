import dataclasses
import json
import logging

from kafka import KafkaProducer  # type: ignore

from .checker import CheckResult

logger = logging.getLogger(__name__)


class Sender:
    def __init__(self, topic: str, producer: KafkaProducer):
        self._topic = topic
        self._producer = producer

    def send(self, result: CheckResult) -> None:
        self._producer.send(
            self._topic, json.dumps(dataclasses.asdict(result)).encode()
        ).add_callback(on_send_success).add_errback(on_send_error)


def on_send_success(_record_metadata):
    logger.info("Message sent")


def on_send_error(excp):
    logger.error("Couldn't send the message", exc_info=excp)
