import dataclasses
import json
import logging
from typing import Optional

from kafka import KafkaConsumer, KafkaProducer  # type: ignore

from .checker import CheckResult

logger = logging.getLogger(__name__)


class Sender:
    def __init__(self, topic: str, producer: KafkaProducer):
        self._topic = topic
        self._producer = producer

    def send(self, result: CheckResult) -> None:
        """ Publish the content of the check result on the provided topic """
        logger.info("Publishing message %s to topic %s", result, self._topic)
        self._producer.send(
            self._topic, json.dumps(dataclasses.asdict(result)).encode()
        ).add_callback(on_send_success).add_errback(on_send_error)


def on_send_success(_record_metadata):
    logger.info("Message sent")


def on_send_error(excp):
    logger.error("Couldn't send the message", exc_info=excp)


class Receiver:
    def __init__(self, topic: str, consumer: KafkaConsumer):
        self._topic = topic
        self._consumer = consumer

    def __iter__(self):
        self._consumer.subscribe(self._topic)
        return self

    def __next__(self) -> Optional[CheckResult]:
        while True:
            message = next(self._consumer).value
            try:
                return CheckResult(**json.loads(message))
            except TypeError:
                logger.warning("Ignoring the message %s", message)
