from docker.models.containers import Container
from docker.models.services import Service

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class CpuAndMemoryLimitsChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        services = self.docker_client.services.list()
        are_only_containers_with_limits = True
        for service in services:
            has_container_cpu_limit = self.__has_container_cpu_limit(service)
            has_container_memory_limit = self.__has_container_memory_limit(service)

            if not has_container_cpu_limit and not has_container_memory_limit:
                self.logger.warning(f"No CPU and memory limits are set for the service {service.id}. Please set the "
                                  f"limits.")
                are_only_containers_with_limits = False
            elif not has_container_cpu_limit:
                self.logger.warning(f"No CPU limit is set for the service {service.id}. Please set the CPU limit.")
                are_only_containers_with_limits = False
            elif not has_container_memory_limit:
                self.logger.warning(f"No memory limit is set for the service {service.id}. Please set the memory limit.")
                are_only_containers_with_limits = False

        if are_only_containers_with_limits:
            self.logger.info("All of the containers have CPU and memory limits set.")
            return CheckerResult.PASSED

        else:
            return CheckerResult.FAILED

    def __has_container_memory_limit(self, service: Service) -> bool:
        limits = self.__get_limits(service)
        return "MemoryBytes" in limits

    def __has_container_cpu_limit(self, service: Service) -> bool:
        limits = self.__get_limits(service)
        return "NanoCPUs" in limits

    def __get_limits(self, service: Service) -> dict:
        resources = service.attrs.get('Spec').get('TaskTemplate').get('Resources')
        return resources.get('Limits') if 'Limits' in resources else {}
