from docker import DockerClient
from docker.models.containers import Container
from functional import seq
from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class RestartPolicyChecker(BaseChecker):
    HOST_CONFIG_PROPERTY_NAME = "HostConfig"
    RESTART_POLICY_PROPERTY_NAME = "RestartPolicy"
    RESTART_POLICY_NAME_PROPERTY_NAME = "Name"
    RESTART_POLICY_MAX_RETRY_COUNT_PROPERTY_NAME = "MaximumRetryCount"

    def __init__(self, docker_client: DockerClient):
        self.docker_client = docker_client

    def run_checker(self):
        containers = self.docker_client.containers.list()
        failed_containers = seq(containers) \
            .map(self.__check_container_restart_policy) \
            .filter(lambda result: result[0] is False)

        if failed_containers.count() > 0:
            messages = failed_containers.map(lambda result: result[1])
            return CheckerResult(0, self.__generate_message(messages))

    def __check_container_restart_policy(self, container: Container):
        error_info = ""
        test_passed = True
        restart_policy = container.attrs \
            .get(self.HOST_CONFIG_PROPERTY_NAME) \
            .get(self.RESTART_POLICY_PROPERTY_NAME)
        restart_policy_name = restart_policy.get(self.RESTART_POLICY_NAME_PROPERTY_NAME).lower()
        restart_policy_max_retry_count = restart_policy.get(self.RESTART_POLICY_MAX_RETRY_COUNT_PROPERTY_NAME)

        if restart_policy_name != "yes":
            error_info = f"Restart policy for container {container.id} is not enabled! You should enable this policy " \
                         f"and set the maximum retry count property to 5 or lower."
            test_passed = False

        elif restart_policy_max_retry_count > 5:
            error_info = f"Maximum retry count for container {container.id} is set to {restart_policy_max_retry_count}" \
                         f"Consider changing it to 5 or lower."
            test_passed = False

        return test_passed, error_info

    def __generate_message(self, messages):
        error_message = ""
        for message in messages:
            error_message += message + "\n"

        return error_message
