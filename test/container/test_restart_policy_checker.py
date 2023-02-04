import unittest
from checker.container.restart_policy_checker import RestartPolicyChecker
from checker.result.checker_result import CheckerResult
from checker.result.result_type import ResultType
from test.fakeapi.fake_api_client import make_fake_client
from test.config.container_configs import valid_container_config, container_config_invalid_restart_policy, \
    container_config_invalid_max_retry_count, FAKE_CONTAINER_ID, INVALID_MAX_RETRY_COUNT


class RestartPolicyCheckerTest(unittest.TestCase):
    EMPTY_MESSAGE = ""
    INVALID_RESTART_POLICY_MESSAGE = f"Restart policy for container {FAKE_CONTAINER_ID} is not set to on-failure! You" \
                                     f" should set this policy and set the maximum retry count property to 5 or lower.\n"
    INVALID_MAX_RETRY_COUNT_MESSAGE = f"Maximum retry count for container {FAKE_CONTAINER_ID} is set to " \
                                      f"{INVALID_MAX_RETRY_COUNT}. It should be set to 5 or lower.\n"

    def test_checker_should_return_no_error_and_empty_message_for_valid_configuration(self):
        config = {
            'containers.return_value': valid_container_config,
            'inspect_container.return_value': valid_container_config
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)
        result = restart_policy_checker.run_checker()
        expected_result = CheckerResult(ResultType.PASSED, self.EMPTY_MESSAGE)
        self.assertEqual(result, expected_result)

    def test_checker_should_return_error_and_appropriate_message_for_invalid_restart_policy(self):
        config = {
            'containers.return_value': container_config_invalid_restart_policy,
            'inspect_container.return_value': container_config_invalid_restart_policy
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)
        result = restart_policy_checker.run_checker()
        expected_result = CheckerResult(ResultType.FAILED, self.INVALID_RESTART_POLICY_MESSAGE)
        self.assertEqual(result, expected_result)

    def test_checker_should_return_error_and_appropriate_message_for_invalid_max_retry_count(self):
        config = {
            'containers.return_value': container_config_invalid_max_retry_count,
            'inspect_container.return_value': container_config_invalid_max_retry_count
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)
        result = restart_policy_checker.run_checker()
        expected_result = CheckerResult(ResultType.FAILED, self.INVALID_MAX_RETRY_COUNT_MESSAGE)
        self.assertEqual(result, expected_result)