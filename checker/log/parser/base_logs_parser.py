from abc import ABC, abstractmethod


class BaseLogsParser(ABC):

    @abstractmethod
    def check_logs_for_errors_in_last_day(self) -> list[str]:
        pass