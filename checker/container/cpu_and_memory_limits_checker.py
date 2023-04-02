from docker.models.containers import Container

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class CpuAndMemoryLimitsChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        are_only_containers_with_limits = True
        for container in containers:
            has_container_cpu_limit = self.__has_container_cpu_limit(container)
            has_container_memory_limit = self.__has_container_memory_limit(container)

            if not has_container_cpu_limit and not has_container_memory_limit:
                self.logger.warning(f"No CPU and memory limits are set for the container {container.id}. Please set the "
                                  f"limits for this container.")
                are_only_containers_with_limits = False
            elif not has_container_cpu_limit:
                self.logger.warning(f"No CPU limit is set for the container {container.id}. Please set the CPU limit for"
                                  f" this container.")
                are_only_containers_with_limits = False
            elif not has_container_memory_limit:
                self.logger.warning(f"No memory limit is set for the container {container.id}. Please set the CPU limit "
                                  f"for this container.")
                are_only_containers_with_limits = False

        if are_only_containers_with_limits:
            self.logger.info("All of the containers have CPU and memory limits set.")
            return CheckerResult.PASSED

        else:
            return CheckerResult.FAILED

    def __has_container_memory_limit(self, container: Container) -> bool:
        memory_limit = container.attrs.get('HostConfig').get('Memory')
        return memory_limit is not None and memory_limit > 0

    def __has_container_cpu_limit(self, container: Container) -> bool:
        cpu_limit = container.attrs.get('HostConfig').get('NanoCpus')
        return cpu_limit is not None and cpu_limit > 0
