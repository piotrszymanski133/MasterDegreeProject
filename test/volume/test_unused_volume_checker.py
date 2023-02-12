import unittest

from checker.result.checker_result import CheckerResult
from checker.volume.unused_volume_checker import UnusedVolumeChecker
from logger.formatter import get_logger
from test.config.container_configs import volume_config, valid_container_config_with_volume_attached, \
    valid_container_config_without_volumes_attached
from test.fakeapi.fake_api_client import make_fake_client


class UnusedVolumeCheckerTest(unittest.TestCase):
    VALID_CONFIGURATION_MESSAGE = "INFO:UnusedVolumeChecker:There are no unused volumes!"
    UNUSED_VOLUME_ERROR_MESSAGE = "ERROR:UnusedVolumeChecker:Volume TestVolume is not attached to any container!"
    log = get_logger(UnusedVolumeChecker.__class__.__name__)

    def test_checker_should_pass_and_log_no_error_message_for_valid_volumes(self):
        config = {
            'containers.return_value': valid_container_config_with_volume_attached,
            'inspect_container.return_value': valid_container_config_with_volume_attached,
            'volumes.return_value': volume_config,
            'inspect_volume.return_value': volume_config
        }
        docker_client = make_fake_client(config)
        unused_volume_checker = UnusedVolumeChecker(docker_client)
        with self.assertLogs(unused_volume_checker.logger) as cm:
            result = unused_volume_checker.run_checker()
            expected_result = CheckerResult.PASSED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.VALID_CONFIGURATION_MESSAGE], cm.output)

    def test_checker_should_fail_and_log_error_message_for_unused_volume(self):
        config = {
            'containers.return_value': valid_container_config_without_volumes_attached,
            'inspect_container.return_value': valid_container_config_without_volumes_attached,
            'volumes.return_value': volume_config,
            'inspect_volume.return_value': volume_config
        }
        docker_client = make_fake_client(config)
        unused_volume_checker = UnusedVolumeChecker(docker_client)
        with self.assertLogs(unused_volume_checker.logger) as cm:
            result = unused_volume_checker.run_checker()
            expected_result = CheckerResult.FAILED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.UNUSED_VOLUME_ERROR_MESSAGE], cm.output)

