from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Check:
    WHITE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3

    # Epoch seconds
    timestamp: int = 0
    type: str = "check"
    uuid: str = ""
    name: str = "<Unknown>"
    status: int = WHITE
    # Duration of the check in ms
    duration: int = 0
    # Has the status changed?
    changed: int = 0
    # The period since the last chnage in s
    period: int = 0
    description: str = ""

    def clone(self):
        clone = Check()
        clone.timestamp = self.timestamp
        clone.type = self.type
        clone.uuid = self.uuid
        clone.name = self.name
        clone.status = self.status
        clone.duration = self.duration
        clone.changed = self.changed
        clone.period = self.period
        clone.description = self.description

        return clone

    def encode(self) -> str:
        txt = f"""timestamp: {self.timestamp}
type: {self.type}
uuid: {self.uuid}
name: {self.name}
status: {self.status}
duration: {self.duration}
changed: {self.changed}
period: {self.period}

{self.description}
"""
        return txt

    def decode(self, txt: str) -> None:
        in_header = True

        for line in txt.splitlines():
            line = line.strip()
            if in_header:
                if len(line) == 0:
                    in_header = False
                    self.description = ""
                elif line.startswith("timestamp: "):
                    self.timestamp = int(line.split(": ")[1])
                elif line.startswith("type: "):
                    self.type = str(line.split(": ")[1])
                elif line.startswith("uuid: "):
                    self.uuid = str(line.split(": ")[1])
                elif line.startswith("name: "):
                    self.name = str(line.split(": ")[1])
                elif line.startswith("status: "):
                    self.status = int(line.split(": ")[1])
                elif line.startswith("duration: "):
                    self.duration = int(line.split(": ")[1])
                elif line.startswith("changed: "):
                    self.changed = int(line.split(": ")[1])
                elif line.startswith("period: "):
                    self.period = int(line.split(": ")[1])
                else:
                    raise Exception(f"Unknown header: {line}")
            else:
                self.description += line
