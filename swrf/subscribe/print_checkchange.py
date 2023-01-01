import logging
import time

import stomp
from stomp import ConnectionListener

from swrf.check import CheckChange, checkchange_decode
from swrf.config import config

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "01 januari 2023"

logger = logging.getLogger(__name__)


class CheckChangeListener(ConnectionListener):
    def on_error(self, frame):
        logger.error(f"received an error: {frame}")

    def on_message(self, frame):
        change = checkchange_decode(frame.body)

        if change.status == CheckChange.GREEN:
            logger.info(f"{change.name}: Changed to Green - {change.duration} s")
        elif change.status == CheckChange.YELLOW:
            logger.warning(f"{change.name}: Changed to Yellow - {change.duration} s")
        elif change.status == CheckChange.RED:
            logger.error(f"{change.name}: Changed to Red - {change.duration} s")


def main() -> None:
    logger.debug("main() - start")

    conn = stomp.Connection(
        [
            (config["ACTIVEMQ_HOSTNAME"], config["ACTIVEMQ_PORT"]),
        ]
    )
    conn.set_listener("printCheck", CheckChangeListener())
    conn.connect(config["ACTIVEMQ_USERNAME"], config["ACTIVEMQ_PASSWORD"], wait=True)
    logger.info("Connect...")
    conn.subscribe(config["ACTIVEMQ_TOPIC_CHANGE"], id=1, ack="auto")

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
