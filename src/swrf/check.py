from dataclasses import dataclass
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

    @staticmethod
    def decode(txt: str) -> "Check":
        chck = Check()
        in_header = True

        for line in txt.splitlines():
            line = line.strip()
            if in_header:
                if len(line) == 0:
                    in_header = False
                    chck.description = ""
                elif line.startswith("timestamp: "):
                    chck.timestamp = int(line.split(": ")[1])
                elif line.startswith("type: "):
                    chck.type = str(line.split(": ")[1])
                elif line.startswith("uuid: "):
                    chck.uuid = str(line.split(": ")[1])
                elif line.startswith("name: "):
                    chck.name = str(line.split(": ")[1])
                elif line.startswith("status: "):
                    chck.status = int(line.split(": ")[1])
                elif line.startswith("duration: "):
                    chck.duration = int(line.split(": ")[1])
                elif line.startswith("changed: "):
                    chck.changed = int(line.split(": ")[1])
                elif line.startswith("period: "):
                    chck.period = int(line.split(": ")[1])
                else:
                    raise Exception(f"Unknown header: {line}")
            else:
                chck.description += line

        return chck
