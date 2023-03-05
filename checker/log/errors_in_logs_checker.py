from datetime import datetime, timedelta
from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class ErrorsInLogsChecker(BaseChecker):

    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        passed = True
        for container in containers:
            timestamp_day_ago = datetime.utcnow() - timedelta(days=1)
            error_logs_bytes = container.logs(stdout=False, stderr=True, timestamps=True, since=timestamp_day_ago)
            error_logs = error_logs_bytes.decode('utf-8')
            if error_logs is not "":
                error_logs_list = error_logs.split(sep="\n")
                filtered_error_logs = self.__filter_error_logs(error_logs_list)
                if filtered_error_logs != "":
                    passed = False
                    self.logger.error(f"Found error logs in the last 24h for the container {container.id}:\n{filtered_error_logs}")

        if passed:
            self.logger.info("Din not found any errors in container logs from last 24h!")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED

    def __filter_error_logs(self, log_list):
        filtered_list = [s for s in log_list if "error" in s.lower()]
        return "\n".join(filtered_list)
