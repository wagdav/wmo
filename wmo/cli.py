from pathlib import Path
import argparse
import logging
import sys
import time

from kafka import KafkaConsumer, KafkaProducer  # type: ignore

from wmo.checker import Checker
from wmo.messenger import Receiver, Sender
from wmo.db import Writer


def kafka_creds(creds_dir: Path):
    """
    Create Kafka connection parameters by reading the necessary files from the
    following layout on the file system:

    └── kafka-389b7aa7-wagdav-b825.aivencloud.com:24387
        ├── ca.pem
        ├── service.cert
        └── service.key

    The return dictionary can be passed to the constructors of KafkaConsumer
    and KafkaProducer.
    """
    creds_dir = Path(creds_dir)
    return {
        "bootstrap_servers": creds_dir.name,
        "security_protocol": "SSL",
        "ssl_cafile": str(creds_dir / "ca.pem"),
        "ssl_certfile": str(creds_dir / "service.cert"),
        "ssl_keyfile": str(creds_dir / "service.key"),
    }


def check():
    parser = argparse.ArgumentParser(description="Check website availability")
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        metavar="SECONDS",
        help="check interval in seconds",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        metavar="REGEXP",
        help="Match the regular expression pattern in the response body",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="wmo",
        help="Publish the website check results under this topic",
    )
    parser.add_argument(
        "--kafka",
        type=str,
        required=True,
        metavar="PATH",
        help="Read the service configuration from this path.",
    )
    parser.add_argument(
        "urls", nargs="+", type=str, metavar="URL", help="address of the website"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        checker = Checker(timeout=5, pattern=args.pattern)
        sender = Sender(args.topic, KafkaProducer(**kafka_creds(args.kafka)))

        while True:
            results = checker.check_sites(args.urls)
            for result in results:
                sender.send(result)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        logging.exception("Unexpected error")
        sys.exit(1)


def write():
    parser = argparse.ArgumentParser(
        description="Write website availability results to a database"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="wmo",
        help="Subscribe to website check results on this topic",
    )
    parser.add_argument(
        "--kafka",
        type=str,
        required=True,
        metavar="PATH",
        help="Read the service configuration from this path.",
    )
    parser.add_argument(
        "--db",
        type=str,
        metavar="URI",
        help="PostgreSQL database connection string.",
    )
    parser.add_argument(
        "--table",
        type=str,
        default="wmo",
        help="Write the results into this table",
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        for result in Receiver(args.topic, KafkaConsumer(**kafka_creds(args.kafka))):
            if args.db:
                Writer(args.db).write(args.table, result)
            else:
                print(result)

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        logging.exception("Unexpected error")
        sys.exit(1)
