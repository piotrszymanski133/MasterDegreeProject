from docker.models.containers import Container

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class CpuAndMemoryLimitsChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        tasks = self.docker_client.api.tasks(filters={'desired-state': 'running'})
        are_only_containers_with_limits = True
        for task in tasks:
            has_container_cpu_limit = self.__has_container_cpu_limit(task)
            has_container_memory_limit = self.__has_container_memory_limit(task)
            status = task.get('Status')
            if 'ContainerStatus' not in status:
                continue
            container_id = status.get('ContainerStatus').get('ContainerID')

            if not has_container_cpu_limit and not has_container_memory_limit:
                self.logger.warning(f"No CPU and memory limits are set for the container {container_id}. Please set the "
                                  f"limits.")
                are_only_containers_with_limits = False
            elif not has_container_cpu_limit:
                self.logger.warning(f"No CPU limit is set for the container {container_id}. Please set the CPU limit.")
                are_only_containers_with_limits = False
            elif not has_container_memory_limit:
                self.logger.warning(f"No memory limit is set for the container {container_id}. Please set the memory limit.")
                are_only_containers_with_limits = False

        if are_only_containers_with_limits:
            self.logger.info("All of the containers have CPU and memory limits set.")
            return CheckerResult.PASSED

        else:
            return CheckerResult.FAILED

    def __has_container_memory_limit(self, task: dict) -> bool:
        limits = self.__get_limits(task)
        return "MemoryBytes" in limits

    def __has_container_cpu_limit(self, task: dict) -> bool:
        limits = self.__get_limits(task)
        return "NanoCPUs" in limits

    def __get_limits(self, task: dict) -> dict:
        resources = task.get('Spec').get('Resources')
        return resources.get('Limits') if 'Limits' in resources else {}
