import unittest
from checker.container.restart_policy_checker import RestartPolicyChecker
from checker.result.checker_result import CheckerResult
from logger.formatter import get_logger
from test.fakeapi.fake_api_client import make_fake_client
from test.config.container_configs import valid_container_config_without_volumes_attached, container_config_invalid_restart_policy, \
    container_config_invalid_max_retry_count, FAKE_CONTAINER_ID, INVALID_MAX_RETRY_COUNT


class RestartPolicyCheckerTest(unittest.TestCase):
    INVALID_RESTART_POLICY_MESSAGE = f'ERROR:RestartPolicyChecker:Restart policy for container {FAKE_CONTAINER_ID} ' \
                                     f'is not set to on-failure! You should set this policy and set the maximum retry' \
                                     f' count property to 5 or lower.'
    INVALID_MAX_RETRY_COUNT_MESSAGE = f'ERROR:RestartPolicyChecker:Maximum retry count for container {FAKE_CONTAINER_ID}' \
                                      f' is set to {INVALID_MAX_RETRY_COUNT}. It should be set to 5 or lower.'
    VALID_CONFIGURATION_MESSAGE = "INFO:RestartPolicyChecker:Restart policies are set properly"
    log = get_logger(RestartPolicyChecker.__class__.__name__)

    def test_checker_should_pass_and_log_valid_configuration_message_for_valid_configuration(self):
        config = {
            'containers.return_value': valid_container_config_without_volumes_attached,
            'inspect_container.return_value': valid_container_config_without_volumes_attached
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)

        with self.assertLogs(restart_policy_checker.logger) as cm:
            result = restart_policy_checker.run_checker()
            expected_result = CheckerResult.PASSED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.VALID_CONFIGURATION_MESSAGE], cm.output)

    def test_checker_should_fail_and_log_appropriate_message_for_invalid_restart_policy(self):
        config = {
            'containers.return_value': container_config_invalid_restart_policy,
            'inspect_container.return_value': container_config_invalid_restart_policy
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)
        with self.assertLogs(restart_policy_checker.logger) as cm:
            result = restart_policy_checker.run_checker()
            expected_result = CheckerResult.FAILED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.INVALID_RESTART_POLICY_MESSAGE], cm.output)

    def test_checker_should_fail_and_log_appropriate_message_for_invalid_max_retry_count(self):
        config = {
            'containers.return_value': container_config_invalid_max_retry_count,
            'inspect_container.return_value': container_config_invalid_max_retry_count
        }
        docker_client = make_fake_client(config)
        restart_policy_checker = RestartPolicyChecker(docker_client)
        with self.assertLogs(restart_policy_checker.logger) as cm:
            result = restart_policy_checker.run_checker()
            expected_result = CheckerResult.FAILED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.INVALID_MAX_RETRY_COUNT_MESSAGE], cm.output)