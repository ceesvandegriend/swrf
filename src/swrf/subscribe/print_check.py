import logging
import time

import stomp
from stomp import ConnectionListener

from swrf.check import Check
from swrf.config import config

logger = logging.getLogger(__name__)


class CheckListener(ConnectionListener):
    def on_error(self, frame):
        logger.error(f"received an error: {frame}")

    def on_message(self, frame):
        chck = Check()
        chck.decode(frame.body)

        if chck.status == Check.GREEN and chck.changed == 0:
            logger.info(f"{chck.name}: Green - {chck.duration} ms / {chck.period} s")
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


def main() -> None:
    logger.debug("main() - start")

    conn = stomp.Connection(
        [
            (config["ACTIVEMQ_HOSTNAME"], config["ACTIVEMQ_PORT"]),
        ]
    )
    conn.set_listener("printCheck", CheckListener())
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
