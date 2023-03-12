from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class NumberOfMasterNodesChecker(BaseChecker):

    def run_checker(self) -> CheckerResult:
        nodes = self.docker_client.nodes.list()
        manager_nodes_count = 0
        for node in nodes:
            node_role = node.attrs.get('Spec').get('Role')
            if node_role.lower() == 'manager':
                manager_nodes_count += 1

        if manager_nodes_count % 2 == 0 or manager_nodes_count > 7:
            self.logger.warning(f"The number of manager nodes equals {manager_nodes_count} which is invalid! "
                              f"Swarm should include an odd number and less than 8 manager nodes")
            return CheckerResult.FAILED

        else:
            self.logger.info(f"The number of manager nodes equals {manager_nodes_count} which is valid!")
            return CheckerResult.PASSED