from docker import DockerClient
from docker.models.containers import Container
from docker.models.volumes import Volume

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class UnusedVolumeChecker(BaseChecker):

    def __init__(self, docker_client: DockerClient):
        super().__init__(docker_client)

    def run_checker(self) -> CheckerResult:
        volumes = self.docker_client.volumes.list()
        containers = self.docker_client.containers.list()
        unattached_volumes = []
        for volume in volumes:
            if self.__is_volume_unattached(volume,containers):
                unattached_volumes.append(volume)

        if len(unattached_volumes) > 0:
            return CheckerResult.FAILED
        else:
            self.logger.info("There are no unused volumes.")
            return CheckerResult.PASSED

    def __is_volume_unattached(self, volume: Volume, containers: list[Container]) -> bool:
        containers_attached_to_volume = []
        for container in containers:
            container_mounts = container.attrs.get('Mounts')
            if self.__is_volume_attached_to_container(volume, container_mounts):
                containers_attached_to_volume.append(container)

        if len(containers_attached_to_volume) == 0:
            self.logger.warning(f"Volume {volume.name} is not attached to any container. Please consider removing it or"
                                f" attaching it to an appropriate container.")
            return True

        return False

    def __is_volume_attached_to_container(self, volume: Volume, container_mounts: list[dict]) -> bool:
        for container_mount in container_mounts:
            if container_mount.get('Name') == volume.name:
                return True
        return False

