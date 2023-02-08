from enum import Enum


class ResultType(Enum):
    PASSED = 0,
    PASSED_WITH_WARNINGS = 1,
    FAILED = 2
