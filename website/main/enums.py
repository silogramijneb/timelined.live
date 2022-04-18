
from enum import Enum

class EventStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    ACTION_WAITING = 2
    COMPLETE = 3