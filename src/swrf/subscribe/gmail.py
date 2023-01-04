# ToDo: logging

import random
import smtplib
import ssl
import time
import uuid

from swrf.check import Check
from swrf.config import config

receivers = [
    "cees+swrf@griend.eu",
    "liesbethopen@gmail.com",
]


def email(check: Check, rx: str) -> None:
    tx = config["GMAIL_USERNAME"]
    password = config["GMAIL_PASSWORD"]
    port = 465

    msg = f"""From: Cees van de Griend (Check) <{tx}>
To: {rx}
Subject: Check {check.name}

{check.encode()}
"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(tx, password)
        server.sendmail(tx, rx, msg)
        server.quit()


def gmail(check: Check) -> None:
    for rx in receivers:
        email(check, rx)


if __name__ == "__main__":
    check = Check()
    check.timestamp = int(time.time())
    check.type = "test"
    check.uuid = uuid.uuid4()
    check.name = "Test"
    check.status = Check.GREEN
    check.duration = random.randint(100, 200)
    check.changed = 0
    check.period = random.randint(60, 3600)
    check.description = "Just a silly check"

    gmail(check)
