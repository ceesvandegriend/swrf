from datetime import datetime
import logging
import time
import uuid
import urllib3
import urllib3.exceptions

import requests
from requests.exceptions import ConnectionError
import stomp

from swrf.check import Check, CheckChange, check_encode, checkchange_encode
from swrf.config import config

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "01 januari 2023"

logger = logging.getLogger(__name__)


def check(id: str, name: str, url: str) -> Check:
    logger.debug("check() - start")

    check = Check()
    check.uuid = id
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
            conn.send(
                body=check_encode(chck), destination=config["ACTIVEMQ_TOPIC_CHECK"]
            )

            if chck.status == Check.GREEN:
                logger.info(f"{chck.name}: Green - {chck.duration} ms")
            elif chck.status == Check.YELLOW:
                logger.warning(f"{chck.name}: Yellow - {chck.duration} ms")
            elif chck.status == Check.RED:
                logger.error(f"{chck.name}: Red - {chck.duration} ms")

            if saved:
                # Not new
                if saved.status != chck.status:
                    # Changed
                    change = CheckChange(chck)
                    change.type = "change"
                    change.duration = saved.timestamp - chck.timestamp
                    conn.send(
                        body=checkchange_encode(change),
                        destination=config["ACTIVEMQ_TOPIC_CHANGE"],
                    )

                    if change.status == Check.GREEN:
                        logger.info(
                            f"{change.name}: Changed to Green - {change.duration} s"
                        )
                    elif chck.status == Check.YELLOW:
                        logger.warning(
                            f"{change.name}: Changed to Yellow - {change.duration} s"
                        )
                    elif chck.status == Check.RED:
                        logger.error(
                            f"{change.name}: Changed to Red - {change.duration} s"
                        )
            else:
                # New
                change = CheckChange(chck)
                change.type = "change"
                change.duration = 0
                conn.send(
                    body=checkchange_encode(change),
                    destination=config["ACTIVEMQ_TOPIC_CHANGE"],
                )
                saved = chck

                if change.status == Check.GREEN:
                    logger.info(
                        f"{change.name}: Changed to Green - {change.duration} s"
                    )
                elif chck.status == Check.YELLOW:
                    logger.warning(
                        f"{change.name}: Changed to Yellow - {change.duration} s"
                    )
                elif chck.status == Check.RED:
                    logger.error(f"{change.name}: Changed to Red - {change.duration} s")

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
