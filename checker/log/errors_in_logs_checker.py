from docker.models.containers import Container

from checker.base_checker import BaseChecker
from checker.log.determiner.container_base_image_determiner import ContainerBaseImageDeterminer
from checker.log.parser.logs_parser_factory import LogsParserFactory
from checker.result.checker_result import CheckerResult


class ErrorsInLogsChecker(BaseChecker):
    logs_parser_factory = LogsParserFactory()
    image_determiner = ContainerBaseImageDeterminer()

    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        for container in containers:
            base_image = self.__check_container_image(container)
            if base_image is not 'Unknown':
                logs_parser = self.logs_parser_factory.get_parser_for_image(base_image)
                errors = logs_parser.check_logs_for_errors_in_last_day(container)

    def __check_container_image(self, container: Container) -> str:
        return self.image_determiner.determine_container_base_image(container)
