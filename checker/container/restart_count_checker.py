from datetime import datetime, timedelta

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class RestartCountChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        passed = True
        for container in containers:
            restarts = 0
            datetime_now = datetime.utcnow()
            datetime_24h_ago = datetime_now - timedelta(days=1)
            events = self.docker_client.api.events(filters={"container": container.id}, decode=True,
                                                   since=datetime_24h_ago, until=datetime_now)
            for event in events:
                if event['status'] == 'restart' or event['status'] == 'start':
                    restarts += 1

            if restarts >= 3:
                self.logger.warning(f"Container {container.id} has restarted {restarts} times in the last 24 hours. "
                                  f"Please check what was the reason.")
                passed = False

        if passed:
            self.logger.info("Did not find any containers with more than 3 restarts in the last 24 hours")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED
