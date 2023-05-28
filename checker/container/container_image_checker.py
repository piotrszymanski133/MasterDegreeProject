from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class ContainerImageChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        passed = True
        for container in containers:
            image = container.attrs.get('Config').get('Image')
            if 'latest' in image:
                passed = False
                self.logger.warning(f"Container {container.id} was started using image with latest tag - {image}."
                                    f" Please use other tag or sha256 hash of the image.")
            elif ':' not in image:
                passed = False
                self.logger.warning(f"Container {container.id} was started using image without specifying tag - {image}."
                                    f" Please use tag or sha256 hash of the image.")

        if passed:
            self.logger.info("All of the containers were started using proper tag or sha256 tag.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED
