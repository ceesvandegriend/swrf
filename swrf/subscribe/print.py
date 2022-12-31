import logging
import time

import stomp
from stomp import listener

from swrf.check import Check, check_decode
from swrf.config import config

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "31 december 2022"

logger = logging.getLogger(__name__)


class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        logger.error(f"received an error: {frame}")

    def on_message(self, frame):
        check = check_decode(frame.body)

        if check.status == Check.GREEN:
            logger.info(f"{check.name}: Green - {check.duration} ms")
        elif check.status == Check.YELLOW:
            logger.warning(f"{check.name}: Green - {check.duration} ms")
        elif check.status == Check.RED:
            logger.error(f"{check.name}: Green - {check.duration} ms")


def main() -> None:
    logger.debug("main() - start")

    conn = stomp.Connection(
        [
            (config["ACTIVEMQ_HOSTNAME"], config["ACTIVEMQ_PORT"]),
        ]
    )
    conn.set_listener("", MyListener())
    conn.connect(config["ACTIVEMQ_USERNAME"], config["ACTIVEMQ_PASSWORD"], wait=True)
    logger.info("Connect...")
    conn.subscribe(config["ACTIVEMQ_QUEUE"], id=1, ack="auto")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Ctrl-C...")
    finally:
        conn.disconnect()
        logger.info("Disconnect...")

    logger.debug("main() - finish")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    stomp_log = logging.getLogger("stomp.py")
    stomp_log.setLevel(logging.ERROR)

    try:
        main()
    except Exception as e:
        logger.exception(e)
