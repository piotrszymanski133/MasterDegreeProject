from docker.models.services import Service

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class RestartPolicyChecker(BaseChecker):

    def run_checker(self) -> CheckerResult:
        passed = True
        services = self.docker_client.services.list()
        service_ids = []
        for service in services:
            service_ids.append(service.id)
            if not self.__is_service_restart_policy_valid(service):
                passed = False

        if passed:
            self.logger.info("Restart policies are set properly.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED

    def __is_service_restart_policy_valid(self, service: Service) -> bool:
        restart_policy = service.attrs.get('Spec').get('TaskTemplate').get('RestartPolicy')

        if type(restart_policy) is not dict:
            error_info = f"Restart policy for service {service.id} is not set! Please set " \
                         f"this policy to on-failure and set the maximum retry count property to 5 or lower."
            self.logger.warning(error_info)
            return False

        restart_condition = restart_policy.get('Condition')
        restart_max_attempts = restart_policy.get('MaxAttempts')
        test_passed = True

        if restart_condition != "on-failure":
            error_info = f"Restart policy for container {service.id} is set to {restart_condition}! Please set " \
                         f"this policy to on-failure and set the maximum retry count property to 5 or lower."
            self.logger.warning(error_info)
            test_passed = False

        elif restart_max_attempts > 5:
            error_info = f"Maximum retry count for service {service.id} is set to {restart_max_attempts}." \
                         f" It should be set to 5 or lower."
            self.logger.warning(error_info)
            test_passed = False

        return test_passed

    def __generate_message(self, messages: str) -> str:
        error_message = ""
        for message in messages:
            error_message += message + "\n"

        return error_message
