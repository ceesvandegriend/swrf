from dataclasses import dataclass
from datetime import datetime

__author__ = "Cees van de Griend <cees@griend.eu>"
__status__ = "development"
__version__ = "0.1"
__date__ = "29 december 2022"


@dataclass
class Check:
    WHITE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3

    time: datetime = datetime.now()
    name: str = "<Unknown>"
    description: str = ""
    status: int = WHITE
    duration: int = 0
