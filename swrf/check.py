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

    uuid: str = ""
    time: datetime = datetime.now()
    name: str = "<Unknown>"
    description: str = ""
    status: int = WHITE
    duration: int = 0
    timestamp: int = 0


def check_encode(check: Check) -> str:
    txt = f"""uuid: {check.uuid}
time: {check.time}
type: check
name: {check.name}
status: {check.status}
duration: {check.duration}
timestamp: {check.time.strftime('%s')}

{check.description}
"""
    return txt


def check_decode(txt: str) -> Check:
    check = Check()
    in_header = True

    for line in txt.splitlines():
        line = line.strip()
        if in_header:
            if len(line) == 0:
                in_header = False
                check.description = ""
            elif line.startswith("uuid:"):
                check.uuid = str(line.split(": ")[1])
            elif line.startswith("time:"):
                check.time = str(line.split(": ")[1])
            elif line.startswith("type:"):
                check.type = str(line.split(": ")[1])
            elif line.startswith("name:"):
                check.name = str(line.split(": ")[1])
            elif line.startswith("status:"):
                check.status = int(line.split(": ")[1])
            elif line.startswith("duration:"):
                check.duration = int(line.split(": ")[1])
            elif line.startswith("timestamp:"):
                check.timestamp = int(line.split(": ")[1])
            else:
                raise Exception(f"Unknown header: {line}")
        else:
            check.description += line

    return check
