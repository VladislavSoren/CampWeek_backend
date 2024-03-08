from enum import Enum


class EventActType(str, Enum):
    all = "all"
    actual = "actual"
    passed = "passed"
