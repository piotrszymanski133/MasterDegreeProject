from docker import DockerClient
from docker.models.containers import Container
from docker.models.volumes import Volume
from functional import seq

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult
from logger.formatter import get_logger


class UnusedVolumeChecker(BaseChecker):

    def __init__(self, docker_client: DockerClient):
        self.docker_client = docker_client
        self.logger = get_logger(self.__class__.__name__)

    def run_checker(self):
        volumes = self.docker_client.volumes.list()
        containers = self.docker_client.containers.list()
        unattached_volumes = seq(volumes)\
            .filter(lambda volume: self.is_volume_unattached(volume, containers))

        if unattached_volumes.len() > 0:
            return CheckerResult.FAILED
        else:
            self.logger.info("There are no unused volumes!")
            return CheckerResult.PASSED

    def is_volume_unattached(self, volume: Volume, containers: list[Container]):
        containers_attached_to_volume = seq(containers)\
            .map(lambda container: container.attrs.get('Mounts'))\
            .filter(lambda mount_points: self.is_volume_attached_to_container(volume, mount_points))

        if containers_attached_to_volume.len() == 0:
            self.logger.error(f"Volume {volume.name} is not attached to any container!")
            return True

        return False


    def is_volume_attached_to_container(self, volume: Volume, container_mounts: list[dict]):
        return seq(container_mounts)\
            .filter(lambda mount_point: mount_point.get('Name') == volume.name)\
            .len() > 0
