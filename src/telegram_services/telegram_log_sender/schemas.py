from typing import NamedTuple
from enum import Enum
from config import settings


class LogLevel(Enum):
    ERROR = 'ERROR'
    INFO = 'INFO'


class LogBody(NamedTuple):
    message: str
    user_id: int
    level: LogLevel
