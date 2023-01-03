import logging
import os
import sqlite3

from swrf.check import Check

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS checks (
    id          INTEGER   NOT NULL PRIMARY KEY AUTOINCREMENT,
    ts          TIMESTAMP NOT NULL,
    type        TEXT      NOT NULL,
    uuid        TEXT      NOT NULL,
    name        TEXT      NOT NULL,
    status      INTEGER   NOT NULL DEFAULT 0,
    duration    INTEGER   NOT NULL DEFAULT 0,
    changed     INTEGER   NOT NULL DEFAULT 0,
    period      INTEGER   NOT NULL DEFAULT 0,
    description TEXT      NOT NULL DEFAULT ''
)
"""

INSERT_CHECK_SQL = """
INSERT INTO checks (
    ts, 
    type, 
    uuid, 
    name, 
    status, 
    duration, 
    changed, 
    period, 
    description
) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


logger = logging.getLogger(__name__)


def get_database_filename():
    home_dir = os.path.expanduser("~")
    db_dir = os.path.join(home_dir, "var", "swrf", "db")
    # Override with environment variable, if exists
    db_dir = os.environ.get("DB_DIR", db_dir)

    if not os.path.isdir(db_dir):
        os.makedirs(db_dir)

    db_filename = os.path.join(db_dir, "swrf.db")

    return db_filename


def database_create(filename: str):
    logger.debug(f"database_create({filename}) - start")

    print(CREATE_TABLE_SQL)

    with sqlite3.connect(filename) as conn:
        with conn as cursor:
            cursor.execute(CREATE_TABLE_SQL)

    logger.debug(f"database_create({filename}) - finish")


def database_insert_check(filename: str, check: Check):
    logger.debug(f"database_insert_check({filename}) - start")

    data = (
        check.timestamp,
        check.type,
        check.uuid,
        check.name,
        check.status,
        check.duration,
        check.changed,
        check.period,
        check.description,
    )

    with sqlite3.connect(filename) as conn:
        with conn as cursor:
            cursor.execute(INSERT_CHECK_SQL, data)

    logger.debug(f"database_insert_check({filename}) - finish")


def main() -> None:
    logger.debug("main() - start")

    filename = get_database_filename()
    database_create(filename)

    logger.debug("main() - finish")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    try:
        main()
    except Exception as e:
        logger.exception(e)
