import unittest

from checker.result.checker_result import CheckerResult
from checker.volume.sensitive_mountpoint_checker import SensitiveMountPointChecker
from test.config.container_configs import volume_config, unsafe_mountpoint_volume_config
from test.fakeapi.fake_api_client import make_fake_client


class SensitiveMountPointCheckerTest(unittest.TestCase):
    VALID_MOUNTPOINT_MESSAGE = "INFO:SensitiveMountPointChecker:All volumes are mounted to a safe, non-sensitive host" \
                               " locations!"
    INVALID_MOUNTPOINT_MESSAGE = "ERROR:SensitiveMountPointChecker:Volume TestUnsafeVolume is mounted to /etc which " \
                                 "is sensitive directory! You should change the mount point to safer location"

    def test_checker_should_pass_and_log_no_error_message_for_valid_volume_mountpoint(self):
        config = {
            'volumes.return_value': volume_config,
            'inspect_volume.return_value': volume_config
        }
        docker_client = make_fake_client(config)
        sensitive_mountpoint_checker = SensitiveMountPointChecker(docker_client)
        with self.assertLogs(sensitive_mountpoint_checker.logger) as cm:
            result = sensitive_mountpoint_checker.run_checker()
            expected_result = CheckerResult.PASSED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.VALID_MOUNTPOINT_MESSAGE], cm.output)

    def test_checker_should_fail_and_log_error_message_for_unsafe_volume_mountpoint(self):
        config = {
            'volumes.return_value': unsafe_mountpoint_volume_config,
            'inspect_volume.return_value': unsafe_mountpoint_volume_config
        }
        docker_client = make_fake_client(config)
        sensitive_mountpoint_checker = SensitiveMountPointChecker(docker_client)
        with self.assertLogs(sensitive_mountpoint_checker.logger) as cm:
            result = sensitive_mountpoint_checker.run_checker()
            expected_result = CheckerResult.FAILED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.INVALID_MOUNTPOINT_MESSAGE], cm.output)
