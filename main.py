import docker

from checker.container.restart_policy_checker import RestartPolicyChecker


def run_checkers():
    docker_client = docker.from_env()
    checker = RestartPolicyChecker(docker_client)
    checker.run_checker()


if __name__ == '__main__':
    run_checkers()

