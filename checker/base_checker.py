from abc import ABC, abstractmethod
from docker import DockerClient
from logger.formatter import get_logger


class BaseChecker(ABC):

    def __init__(self, docker_client: DockerClient):
        self.docker_client = docker_client
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def run_checker(self):
        pass
