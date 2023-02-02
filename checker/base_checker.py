from abc import ABC, abstractmethod


class BaseChecker(ABC):

    @abstractmethod
    def run_checker(self):
        pass
