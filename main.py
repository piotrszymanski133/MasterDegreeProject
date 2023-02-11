import docker

from checker.container.restart_policy_checker import RestartPolicyChecker
from checker.volume.unused_volume_checker import UnusedVolumeChecker


def run_checkers():
    docker_client = docker.from_env()
    checker = UnusedVolumeChecker(docker_client)
    checker2 = RestartPolicyChecker(docker_client)
    checker.run_checker()
    checker2.run_checker()


if __name__ == '__main__':
    run_checkers()

