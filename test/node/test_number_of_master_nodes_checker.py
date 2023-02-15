import unittest

from checker.node.number_of_master_nodes_checker import NumberOfMasterNodesChecker
from checker.result.checker_result import CheckerResult
from test.config.container_configs import master_node_config
from test.fakeapi.fake_api_client import make_fake_client


class NumberOfMasterNodesCheckerTest(unittest.TestCase):
    VALID_MESSAGE = "INFO:NumberOfMasterNodesChecker:The number of manager nodes equals 1 which is valid!"
    INVALID_MESSAGE = "ERROR:NumberOfMasterNodesChecker:The number of manager nodes equals 2 which is invalid! " \
                      "Swarm should include an odd number and less than 8 manager nodes"

    def test_checker_should_pass_and_log_valid_message_for_valid_number_of_master_nodes(self):
        config = {
            'nodes.return_value': master_node_config,
            'inspect_node.return_value': master_node_config
        }
        docker_client = make_fake_client(config)
        number_of_master_nodes_checker = NumberOfMasterNodesChecker(docker_client)

        with self.assertLogs(number_of_master_nodes_checker.logger) as cm:
            result = number_of_master_nodes_checker.run_checker()
            expected_result = CheckerResult.PASSED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.VALID_MESSAGE], cm.output)

    def test_checker_should_fail_and_log_invalid_message_for_invalid_number_of_master_nodes(self):
        config = {
            'nodes.return_value': [master_node_config, master_node_config],
            'inspect_node.return_value': master_node_config
        }
        docker_client = make_fake_client(config)
        number_of_master_nodes_checker = NumberOfMasterNodesChecker(docker_client)

        with self.assertLogs(number_of_master_nodes_checker.logger) as cm:
            result = number_of_master_nodes_checker.run_checker()
            expected_result = CheckerResult.FAILED
            self.assertEqual(expected_result, result)
            self.assertEqual([self.INVALID_MESSAGE], cm.output)