import argparse
import logging
import sys
import time

from wmo.checker import Checker


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
        "urls", nargs="+", type=str, metavar="URL", help="address of the website"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        checker = Checker(timeout=5, pattern=args.pattern)
        while True:
            result = checker.check_sites(args.urls)
            print(result)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        sys.exit(0)


def write():
    print("Running write")
