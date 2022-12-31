"""
Check an URL for connection.

Copyright: (c) 2022 C.A. van de Griend
"""


from datetime import datetime
import logging
import time
import urllib3
import urllib3.exceptions

import requests
from requests.exceptions import ConnectionError
import stomp

from swrf.check import Check, check_encode
from swrf.config import config

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "31 december 2022"

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

    conn = stomp.Connection([(config['ACTIVEMQ_HOSTNAME'], config['ACTIVEMQ_PORT']),])
    conn.connect(config['ACTIVEMQ_USERNAME'], config['ACTIVEMQ_PASSWORD'], wait=True)
    conn.send(body=check_encode(check), destination=config['ACTIVEMQ_QUEUE'])
    conn.disconnect()

    logger.debug("publish() - finish")


def main() -> None:
    logger.debug("main() - start")

    n = config['CHECK_NAME']
    u = config['CHECK_URL']
    c = check(n , u)

    if c.status == Check.GREEN:
        logger.info(f"{n}: Green - {c.duration} ms")
    elif c.status == Check.YELLOW:
        logger.warning(f"{n}: Yellow - {c.duration} ms")
    elif c.status == Check.RED:
        logger.error(f"{n}: Red - {c.duration} ms")

    publish(c)

    logger.debug("main() - finish")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s - %(message)s",)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    stomp_log = logging.getLogger("stomp.py")
    stomp_log.setLevel(logging.ERROR)

    try:
        while True:
            main()
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e)
