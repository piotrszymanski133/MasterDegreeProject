import unittest
from checker.container.restart_policy_checker import RestartPolicyChecker
from checker.result.checker_result import CheckerResult
from checker.result.result_type import ResultType
from test.fakeapi.fake_api_client import make_fake_client
from test.fakeapi.config.container_configs import valid_container_config


class RestartPolicyCheckerTest(unittest.TestCase):
    EMPTY_MESSAGE = ""

    def test_checker_should_return_no_error_and_empty_message_for_valid_configuration(self):
        config = {
            'containers.return_value': valid_container_config,
            'inspect_container.return_value': valid_container_config
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)
        result = restart_policy_checker.run_checker()
        predicted_result = CheckerResult(ResultType.PASSED, self.EMPTY_MESSAGE)
        self.assertEqual(result, predicted_result)
