from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class ContainerImageChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        tasks = self.docker_client.api.tasks(filters={'desired-state': 'running'})
        passed = True
        for task in tasks:
            image = task.get('Spec').get('ContainerSpec').get('Image')
            status = task.get('Status')
            if 'ContainerStatus' not in status:
                continue
            container_id = status.get('ContainerStatus').get('ContainerID')
            if 'latest' in image:
                passed = False
                self.logger.warning(f"Container {container_id} was started using image with latest tag - {image}."
                                    f" Please use other tag or sha256 hash of the image.")
            elif ':' not in image:
                passed = False
                self.logger.warning(f"Container {container_id} was started using image without specifying tag - {image}."
                                    f" Please use tag or sha256 hash of the image.")

        if passed:
            self.logger.info("All of the containers were started using proper tag or sha256 tag.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED
