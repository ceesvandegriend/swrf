"""
Check an URL for connection.

Author:    Cees van de Griend <cees@griend.eu>
Date:      28 dec 2022
Copyright: (c) 2022 C.A. van de Griend
"""
import logging
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning, ConnectTimeoutError

import requests
from requests.exceptions import ConnectTimeout


logger = logging.getLogger(__name__)


def check_url(url: str):
    """
    Check the URL a number of times.

    Returns:
      status_code[] - int
      duration[] - float
    """
    logger.debug("check_url() - start")

    status = []
    duration = []

    for n in range(5):
        t0 = time.perf_counter()
        try:
            response = requests.get(url, verify=False, timeout=0.5)
            status_code = response.status_code
        except InsecureRequestWarning as e:
            pass
        except ConnectTimeout as e:
            status_code = -1
        t1 = time.perf_counter()

        status.append(status_code)
        duration.append(t1 - t0)

    logger.debug("check_url() - finish")

    return status, duration


def checks(name: str, url: str) -> None:
    logger.debug("check() - start")

    statuses, durations = check_url(url)

    success = "Success"
    avg = sum(durations) / len(durations)

    for status in statuses:
        if status != 200:
            success = "Failure"

    logger.info(f"{name} {success} {avg:0.4f}")
    logger.debug("check() - finish")


def check() -> None:
    logger.debug("check() - start")

    checks("UniFi", "https://192.168.1.1/")
    checks("Genexis", "https://192.168.179.1/")
    checks("Google", "https://www.google.nl/")

    logger.debug("check() - finish")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)-12s %(message)s",
    )
    urllib3.disable_warnings(InsecureRequestWarning)

    try:
        check()
    except Exception as e:
        logger.exception(e)
