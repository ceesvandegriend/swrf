from dataclasses import dataclass
from datetime import datetime
import logging

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "01 januari 2023"

logger = logging.getLogger(__name__)


@dataclass
class Check:
    WHITE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3

    timestamp: int = 0
    type: str = "check"
    uuid: str = ""
    name: str = "<Unknown>"
    status: int = WHITE
    duration: int = 0
    description: str = ""


@dataclass
class CheckChange(Check):
    type: str = "change"

    def __init__(self, check: Check):
        super().__init__()
        self.timestamp = check.timestamp
        self.type = "change"
        self.uuid = check.uuid
        self.name = check.name
        self.status = check.status
        self.duration = check.duration
        self.description = check.description


def check_encode(check: Check) -> str:
    txt = f"""timestamp: {check.timestamp}
type: {check.type}
uuid: {check.uuid}
name: {check.name}
status: {check.status}
duration: {check.duration}

{check.description}
"""
    return txt


def checkchange_encode(change: CheckChange) -> str:
    return check_encode(change)


def check_decode(txt: str) -> Check:
    check = Check()
    in_header = True

    for line in txt.splitlines():
        line = line.strip()
        if in_header:
            if len(line) == 0:
                in_header = False
                check.description = ""
            elif line.startswith("timestamp:"):
                check.timestamp = int(line.split(": ")[1])
            elif line.startswith("type:"):
                check.type = str(line.split(": ")[1])
            elif line.startswith("uuid:"):
                check.uuid = str(line.split(": ")[1])
            elif line.startswith("name:"):
                check.name = str(line.split(": ")[1])
            elif line.startswith("status:"):
                check.status = int(line.split(": ")[1])
            elif line.startswith("duration:"):
                check.duration = int(line.split(": ")[1])
            else:
                raise Exception(f"Unknown header: {line}")
        else:
            check.description += line

    return check


def checkchange_decode(txt: str) -> CheckChange:
    return CheckChange(check_decode(txt))
