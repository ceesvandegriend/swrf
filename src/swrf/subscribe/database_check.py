import logging
import os
import time

import stomp
from stomp import ConnectionListener

from swrf.check import Check
from swrf.config import config
from swrf.database import (
    get_database_filename,
    database_create,
    database_insert_check,
)

logger = logging.getLogger(__name__)
running = True


class DatabaseCheckListener(ConnectionListener):
    def on_error(self, frame):
        logger.error(f"received an error: {frame}")

    def on_message(self, frame):
        global running

        try:
            filename = get_database_filename()
            chck = Check()
            chck.decode(frame.body)
            database_insert_check(filename, chck)

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
                logger.error(
                    f"{chck.name}: Red - {chck.duration} ms / {chck.period} s"
                )
            elif chck.status == Check.RED:
                logger.error(
                    f"{chck.name}: Changed to Red - {chck.duration} ms / {chck.period} s"
                )
        except Exception as e:
            logger.exception(e)
            running = False


def main() -> None:
    logger.debug("main() - start")

    global running
    conn = stomp.Connection(
        [
            (config["ACTIVEMQ_HOSTNAME"], config["ACTIVEMQ_PORT"]),
        ]
    )
    conn.set_listener("dbCheck", DatabaseCheckListener())
    conn.connect(
        config["ACTIVEMQ_USERNAME"], config["ACTIVEMQ_PASSWORD"], wait=True
    )
    logger.info("Connect...")
    conn.subscribe(config["ACTIVEMQ_TOPIC"], id=1, ack="auto")

    try:
        logger.info(
            f"ActiveMQ server: {config['ACTIVEMQ_HOSTNAME']}:{config['ACTIVEMQ_PORT']}"
        )
        logger.info(f"Username:        {config['ACTIVEMQ_USERNAME']}")
        logger.info(f"Topic:           {config['ACTIVEMQ_TOPIC']}")

        filename = get_database_filename()
        if not os.path.isfile(filename):
            database_create(filename)
            logger.into(f"Created database: {filename}")

        while running:
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
