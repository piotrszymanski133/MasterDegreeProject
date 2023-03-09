from docker.models.containers import Container

from checker.base_checker import BaseChecker
from checker.container.database_container_detector.database_container_detector import DatabaseContainerDetector
from checker.result.checker_result import CheckerResult


class DbContainerHasVolumeAttachedChecker(BaseChecker):
    database_container_detector = DatabaseContainerDetector()

    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        all_db_containers_have_volumes = True
        for container in containers:
            if self.database_container_detector.is_container_a_db_container(container):
                if not self.__is_volume_attached(container):
                    all_db_containers_have_volumes = False
                    self.logger.error(f"Database container {container.id} don't have a volume attached. Please attach "
                                      f"a volume to this container so the data will be safe")

        if all_db_containers_have_volumes:
            self.logger.info("All of the detected database containers have volumes attached")
            return CheckerResult.PASSED

        else:
            return CheckerResult.FAILED

    def __is_volume_attached(self, container: Container):
        pass
