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
        tasks = self.docker_client.api.tasks()
        unattached_volumes = []
        for volume in volumes:
            if self.__is_volume_unattached(volume, tasks):
                unattached_volumes.append(volume)

        if len(unattached_volumes) > 0:
            return CheckerResult.FAILED
        else:
            self.logger.info("There are no unused volumes.")
            return CheckerResult.PASSED

    def __is_volume_unattached(self, volume: Volume, tasks: list[dict]) -> bool:
        containers_attached_to_volume = []
        for task in tasks:
            container_spec = task.get('Spec')
            if 'Mounts' not in container_spec:
                continue
            mounts = container_spec.get('Mounts')
            if self.__is_volume_attached_to_container(volume, mounts):
                containers_attached_to_volume.append(task)

        if len(containers_attached_to_volume) == 0:
            self.logger.warning(f"Volume {volume.name} is not attached to any container. Please consider removing it or"
                                f" attaching it to an appropriate container.")
            return True

        return False

    def __is_volume_attached_to_container(self, volume: Volume, container_mounts: list[dict]) -> bool:
        for container_mount in container_mounts:
            if container_mount.get('Source') == volume.name:
                return True
        return False

