import docker
import logger.formatter
from checker.base_checker import BaseChecker
from checker.factory.config_reader import get_excluded_checkers


class CheckersFactory:

    def __init__(self):
        self.log = logger.formatter.get_logger(self.__class__.__name__)
        self.docker_client = docker.from_env()

    def create_checkers(self) -> list[BaseChecker]:
        excluded_checkers = get_excluded_checkers()
        checker_classes = BaseChecker.__subclasses__()
        checkers = []
        for checker_class in checker_classes:
            if checker_class.__name__ not in excluded_checkers:
                checker = self.__try_to_initialize_checker(checker_class)
                if checker is not None:
                    checkers.append(checker)
        return checkers

    def __try_to_initialize_checker(self, checker_class: type[BaseChecker]) -> BaseChecker | None:
        try:
            checker = checker_class(self.docker_client)
            return checker
        except:
            self.log.critical(f"An error occured during {checker_class.__name__} initialization")
            return None
