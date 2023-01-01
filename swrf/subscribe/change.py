import logging
import time

import stomp
from stomp import listener

from swrf.check import Check, check_decode
from swrf.config import config

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "01 januari 2023"

logger = logging.getLogger(__name__)

checks = {}


class ChangeListener(stomp.ConnectionListener):
    def on_error(self, frame):
        logger.error(f"received an error: {frame}")

    def on_message(self, frame):
        changed = False
        check = check_decode(frame.body)
        old_check = checks.get(check.uuid)

        if not old_check:
            # New
            changed = True
            checks[check.uuid] = check
            old_check = check
        else:
            if old_check.status == check.status:
                # Unchanged
                changed = False
            else:
                # Changed
                changed = True

        duration = check.timestamp - old_check.timestamp

        if changed and check.status == Check.GREEN:
            logger.info(f"{check.name}: Green - {duration} s")
        elif changed and check.status == Check.YELLOW:
            logger.warning(f"{check.name}: Yellow - {duration} s")
        elif changed and check.status == Check.RED:
            logger.error(f"{check.name}: Red - {duration} s")


def main() -> None:
    logger.debug("main() - start")

    conn = stomp.Connection(
        [
            (config["ACTIVEMQ_HOSTNAME"], config["ACTIVEMQ_PORT"]),
        ]
    )
    conn.set_listener("change", ChangeListener())
    conn.connect(config["ACTIVEMQ_USERNAME"], config["ACTIVEMQ_PASSWORD"], wait=True)
    logger.info("Connect...")
    conn.subscribe(config["ACTIVEMQ_TOPIC"], id=1, ack="auto")

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
