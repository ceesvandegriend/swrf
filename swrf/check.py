"""
Check an URL for connection.

Copyright: (c) 2022 C.A. van de Griend
"""

from dataclasses import dataclass
from datetime import datetime
import logging
import schedule
import time
import urllib3
import urllib3.exceptions

import requests
from requests.exceptions import ConnectionError

from .common import Check
from .database import get_database_filename
from .database import database_insert_check

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "29 december 2022"

logger = logging.getLogger(__name__)


def check(name: str, url: str) -> Check:
    logger.debug("check() - start")

    check = Check()
    check.time = datetime.now()
    check.name = name
    check.description = url

    try:
        t0 = time.perf_counter()
        response = requests.get(url, verify=False, timeout=2.0)
        t1 = time.perf_counter()
        status_code = response.status_code
        duration = round((t1 - t0) * 1000)
    except ConnectionError:
        status_code = 0
        duration = 0

    check.duration = duration

    if status_code <= 0:
        check.status = Check.RED
    elif status_code >= 190 and status_code <= 210:
        check.status = Check.GREEN
    else:
        check.status = Check.YELLOW

    logger.debug("check() - finish")

    return check


def publish(check: Check) -> None:
    logger.debug("publish() - start")

    if check.status == Check.GREEN:
        logger.info(f"{check.name}: Green {check.duration} ms")
    elif check.status == Check.YELLOW:
        logger.warning(f"{check.name}: Yellow {check.duration} ms")
    elif check.status == Check.RED:
        logger.error(f"{check.name}: Red {check.duration} ms")
    else:
        logger.warning(f"{check.name}: White {check.duration} ms")
        logger.warning(check)

    filename = get_database_filename()
    database_insert_check(filename, check)

    logger.debug("publish() - finish")


def main() -> None:
    logger.debug("main() - start")

    publish(check("GW", "https://192.168.128.1/"))
    publish(check("UniFi", "https://192.168.1.1/"))
    publish(check("Genexis", "https://192.168.179.1/"))
    publish(check("Google", "https://www.google.com/"))

    logger.debug("main() - finish")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        main()
        schedule.every(5).minutes.do(main)

        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e)
