from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class ContainerImageChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        services = self.docker_client.services.list()
        passed = True
        for service in services:
            image = service.attrs.get('Spec').get('TaskTemplate').get('ContainerSpec').get('Image')
            if 'latest' in image:
                passed = False
                self.logger.warning(f"Service {service.id} was started using image with latest tag - {image}."
                                    f" Please use other tag or sha256 hash of the image.")

        if passed:
            self.logger.info("All of the containers were started using proper tag or sha256 tag.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED
