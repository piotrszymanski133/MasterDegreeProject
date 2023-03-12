from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class SensitiveMountPointChecker(BaseChecker):
    SENSITIVE_DIRECTORIES = ['/', '/boot', '/dev', '/etc', '/lib', '/proc', '/sys', '/usr']

    def run_checker(self) -> CheckerResult:
        volumes = self.docker_client.volumes.list()
        is_any_unsafe_mountpoint = False
        for volume in volumes:
            mountpoint = volume.attrs.get('Mountpoint')
            if mountpoint in self.SENSITIVE_DIRECTORIES:
                is_any_unsafe_mountpoint = True
                self.logger.warning(f"Volume {volume.id} is mounted to {mountpoint} which is sensitive directory!"
                                  f" You should change the mount point to safer location")

        if is_any_unsafe_mountpoint:
            return CheckerResult.FAILED

        else:
            self.logger.info("All volumes are mounted to a safe, non-sensitive host locations!")
            return CheckerResult.PASSED

