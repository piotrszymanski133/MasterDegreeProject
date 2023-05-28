from datetime import datetime, timedelta

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class RestartCountChecker(BaseChecker):
    TASK_DOWN_STATES = ["failed", "shutdown"]
    def run_checker(self) -> CheckerResult:
        services = self.docker_client.services.list()
        tasks = self.docker_client.api.tasks()

        passed = True
        for service in services:
            datetime_24h_ago = datetime.utcnow() - timedelta(days=1)
            shutdowns = 0
            for task in tasks:
                update_time_iso_format = task.get('UpdatedAt')[0:23]
                task_update_date = datetime.fromisoformat(update_time_iso_format)
                task_desired_state = task.get('DesiredState')
                if task.get('ServiceID') == service.id and task_desired_state in self.TASK_DOWN_STATES and task_update_date > datetime_24h_ago:
                    shutdowns += 1

            if shutdowns > 3:
                self.logger.warning(f"Service {service.id} has  {shutdowns} shutdown or failed tasks in the last "
                                    f"24 hours. Please check what was the reason.")
                passed = False

        if passed:
            self.logger.info("Did not find any containers with more than 3 restarts in the last 24 hours.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED
