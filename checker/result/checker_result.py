from enum import Enum


class CheckerResult(Enum):
    PASSED = 0,
    PASSED_WITH_WARNINGS = 1,
    FAILED = 2

    def __eq__(self, other):
        return self.value == other.value
