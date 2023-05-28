from datetime import datetime, timedelta
from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class ErrorsInLogsChecker(BaseChecker):

    def run_checker(self) -> CheckerResult:
        services = self.docker_client.services.list()
        passed = True
        for service in services:
            timestamp_day_ago = datetime.utcnow() - timedelta(days=1)
            generator = service.logs(stdout=False, stderr=True, since=timestamp_day_ago.timestamp())
            error_logs = [x.decode("utf-8") for x in generator]
            if error_logs != "":
                filtered_error_logs = self.__filter_error_logs(error_logs)
                if filtered_error_logs != "":
                    passed = False
                    self.logger.warning(f"Found error logs in the last 24h for the service {service.id}:\n{filtered_error_logs}")

        if passed:
            self.logger.info("Did not find any errors in container logs from last 24h.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED

    def __filter_error_logs(self, log_list: list[str]):
        severities = ["err", "fatal", "crit", "fail"]
        potential_error_logs = []
        for log in log_list:
            for severity in severities:
                severity_index = log.lower().find(severity)
                if severity_index > -1:
                    if severity_index == 0 or log[severity_index - 1] == " " or log[severity_index - 1] == "\t":
                        potential_error_logs.append(log)
        return "\n".join(err_log for err_log in potential_error_logs)
