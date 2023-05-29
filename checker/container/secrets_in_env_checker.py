from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class SecretsInEnvChecker(BaseChecker):
    def run_checker(self) -> CheckerResult:
        tasks = self.docker_client.api.tasks(filters={'desired-state': 'running'})
        passed = True
        for task in tasks:
            container_spec = task.get('Spec').get('ContainerSpec')
            if 'Env' not in container_spec:
                continue
            envs = container_spec.get('Env')
            potential_secret_envs = self.__detect_potential_secret_envs(envs)
            container_id = task.get('Status').get('ContainerStatus').get('ContainerID')
            for secret_env in potential_secret_envs:
                self.logger.warning(f"Env variable {secret_env} in container {container_id} may contain a hardcoded "
                                  f"secret. Please check it and remove if it really contains a secret.")
                passed = False
                break

        if passed:
            self.logger.info("Did not find any container with environment variables containing potential secrets.")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED

    def __detect_potential_secret_envs(self, envs: list[str]):
        potential_secret_env_keywords = ['PASS', 'KEY', 'SECRET', 'TOKEN']
        non_secret_env_keywords = ['ID', 'LOCATION']
        potential_secret_envs = []
        for env in envs:
            env_name, env_value = env.split('=', 1)
            for keyword in potential_secret_env_keywords:
                if keyword in env_name and not env_value.startswith('/run/secrets/'):
                    false_positive = False
                    for non_secret_keyword in non_secret_env_keywords:
                        if non_secret_keyword in env_name:
                            false_positive = True
                    if not false_positive:
                        potential_secret_envs.append(env_name)

        return potential_secret_envs
