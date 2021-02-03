import argparse
import logging
import sys

import wmo.checker


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
        "urls", nargs="+", type=str, metavar="URL", help="address of the website"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        wmo.checker.periodic(args.urls, args.interval)
    except KeyboardInterrupt:
        sys.exit(0)


def write():
    print("Running write")
