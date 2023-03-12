from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class SecretsInEnvChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        passed = True
        for container in containers:
            envs = container.attrs.get('Config').get('Env')
            potential_secret_envs = self.__detect_potential_secret_envs(envs)
            for secret_env in potential_secret_envs:
                self.logger.warning(f"Env variable {secret_env} in container {container.id} may contain a hardcoded "
                                  f"secret. Please check it and remove if it really contains a secret")
                passed = False

        if passed:
            self.logger.info("Did not found any container with environment variables containing potential secrets!")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED

    def __detect_potential_secret_envs(self, envs: list[str]):
        potential_secret_env_keywords = ['PASS', 'KEY', 'SECRET', 'TOKEN']
        potential_secret_envs = []
        for env in envs:
            env_name, env_value = env.split('=', 1)
            for keyword in potential_secret_env_keywords:
                if keyword in env_name and not env_value.startswith('/run/secrets/'):
                    potential_secret_envs.append(env_name)

        return potential_secret_envs
