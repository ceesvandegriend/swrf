import logging
import time
import uuid
import urllib3
import urllib3.exceptions

import requests
from requests.exceptions import ConnectionError
import stomp

from swrf.check import Check
from swrf.config import config

logger = logging.getLogger(__name__)


def check(id: str, name: str, url: str) -> Check:
    logger.debug("check() - start")

    check = Check()
    check.uuid = id
    check.timestamp = int(time.time())
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
    elif status_code >= 200 and status_code <= 299:
        check.status = Check.GREEN
    else:
        check.status = Check.YELLOW
    logger.debug("check() - finish")

    return check


def main() -> None:
    logger.debug("main() - start")

    id = uuid.uuid4()
    name = config["CHECK_NAME"]
    url = config["CHECK_URL"]
    saved = None
    conn = stomp.Connection(
        [
            (config["ACTIVEMQ_HOSTNAME"], config["ACTIVEMQ_PORT"]),
        ]
    )
    conn.connect(config["ACTIVEMQ_USERNAME"], config["ACTIVEMQ_PASSWORD"], wait=True)

    try:
        while True:
            chck = check(id, name, url)

            if not saved:
                chck.changed = 1
                chck.period = 0
                saved = chck.clone()
            elif saved.status != chck.status:
                chck.changed = 1
                chck.period = chck.timestamp - saved.timestamp
                saved = chck.clone()
            else:
                chck.changed = 0
                chck.period = chck.timestamp - saved.timestamp

            conn.send(body=chck.encode(), destination=config["ACTIVEMQ_TOPIC"])

            if chck.status == Check.GREEN and chck.changed == 0:
                logger.info(
                    f"{chck.name}: Green - {chck.duration} ms / {chck.period} s"
                )
            elif chck.status == Check.GREEN:
                logger.info(
                    f"{chck.name}: Changed to Green - {chck.duration} ms / {chck.period} s"
                )
            elif chck.status == Check.YELLOW and chck.changed == 0:
                logger.warning(
                    f"{chck.name}: Yellow - {chck.duration} ms / {chck.period} s"
                )
            elif chck.status == Check.YELLOW:
                logger.warning(
                    f"{chck.name}: Chanmged to Yellow - {chck.duration} ms / {chck.period} s"
                )
            elif chck.status == Check.RED and chck.changed == 0:
                logger.error(f"{chck.name}: Red - {chck.duration} ms / {chck.period} s")
            elif chck.status == Check.RED:
                logger.error(
                    f"{chck.name}: Changed to Red - {chck.duration} ms / {chck.period} s"
                )

            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        conn.disconnect()

    logger.debug("main() - finish")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    stomp_log = logging.getLogger("stomp.py")
    stomp_log.setLevel(logging.ERROR)

    try:
        main()
    except Exception as e:
        logger.exception(e)
