from checker.result.result_type import ResultType


class CheckerResult:

    def __init__(self, result: ResultType, message: str):
        self.result = result
        self.message = message

    def __eq__(self, other):
        return self.result == other.result and self.message == other.message
