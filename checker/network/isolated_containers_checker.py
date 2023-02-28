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
                if len(network_with_full_info.containers) > 0:
                    filtered_networks.append(network_with_full_info)
            except:
                self.logger.error(f"There was an exception during fetching information about network {network.id}. "
                                  f"Please check it manually")

        results = [self.__is_any_container_from_network_is_accessible_from_outside(network) for network in filtered_networks]
        if results.count(False) == 0:
            self.logger.info("All of the containers are accessible directly or transitively from outside of the Docker")
            return CheckerResult.PASSED

        return CheckerResult.FAILED

    def __is_any_container_from_network_is_accessible_from_outside(self, network: Network):
        network_containers = network.containers
        for container in network_containers:
            for port_in, port_out in container.ports.items():
                if port_out is not None:
                    return True

        inaccessible_containers = []
        for container in network_containers:
            container_networks = container.attrs.get('NetworkSettings').get('Networks')
            for network_name, network_info in container_networks.items():
                network_id_to_check = network_info.get('NetworkID')
                if network_id_to_check != network.id:
                    new_full_network_to_check = self.docker_client.networks.get(network_id_to_check)
                    result = self.__is_any_container_from_network_is_accessible_from_outside(new_full_network_to_check)
                    if result is True:
                        return True
            inaccessible_containers.append(container)

        for inaccessible_container in inaccessible_containers:
            self.logger.error(f"Container {inaccessible_container.id} is not accessible directly or transitively from outside of the Docker")
        return False
