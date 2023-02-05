import docker

from checker.container.restart_policy_checker import RestartPolicyChecker


def run_checkers():
    docker_client = docker.from_env()
    checker = RestartPolicyChecker(docker_client)
    result = checker.run_checker()
    print(result.message)


if __name__ == '__main__':
    run_checkers()

