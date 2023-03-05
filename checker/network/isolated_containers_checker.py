from docker.models.containers import Container
from docker.models.networks import Network

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class IsolatedContainersChecker(BaseChecker):

    def run_checker(self) -> CheckerResult:
        networks = self.docker_client.networks.list()
        filtered_networks = []
        for network in networks:
            try:
                network_with_full_info = self.docker_client.networks.get(network.id)
                if len(network_with_full_info.containers) == 1 or network_with_full_info.name.lower() == "none":
                    filtered_networks.append(network_with_full_info)
            except:
                self.logger.error(f"There was an exception during fetching information about network {network.id}. "
                                  f"Please check it manually")

        results = []
        for network in filtered_networks:
            for container in network.containers:
                results.append(self.__is_container_accessible_from_outside(network, container))
        if results.count(False) == 0:
            self.logger.info("There are no isolated containers in your Docker instance!")
            return CheckerResult.PASSED

        return CheckerResult.FAILED

    def __is_container_accessible_from_outside(self, network: Network, network_container: Container):
        for port_in, port_out in network_container.ports.items():
            if port_out is not None:
                return True

        container_networks = network_container.attrs.get('NetworkSettings').get('Networks')
        for network_name, network_info in container_networks.items():
            network_id_to_check = network_info.get('NetworkID')
            if network_id_to_check != network.id:
                new_full_network_to_check = self.docker_client.networks.get(network_id_to_check)
                if len(new_full_network_to_check.containers) == 1:
                    result = self.__is_container_accessible_from_outside(new_full_network_to_check, network_container)
                    if result is True:
                        return True

        if len(network_container.attrs.get('Mounts')) > 0:
            return True

        self.logger.error(f"Container {network_container.id} is isolated! It does not have any network connection with "
                          f"other containers, it does not map any ports, and does not have any volumes attached.")
        return False
