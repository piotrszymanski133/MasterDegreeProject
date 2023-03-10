from docker import DockerClient
from docker.models.containers import Container

from checker.base_checker import BaseChecker
from checker.result.checker_result import CheckerResult


class DbContainerHasVolumeAttachedChecker(BaseChecker):

    def run_checker(self) -> CheckerResult:
        containers = self.docker_client.containers.list()
        all_db_containers_have_volumes = True
        found_db_container = False
        for container in containers:
            if self.__is_container_a_db_container(container):
                found_db_container = True
                if not self.__is_volume_attached(container):
                    all_db_containers_have_volumes = False
                    self.logger.error(f"Database container {container.id} don't have a volume attached. Please attach "
                                      f"a volume to this container so the data will be safe")

        if not found_db_container:
            self.logger.info("Did not detect any database container!")
            return CheckerResult.PASSED
        elif all_db_containers_have_volumes:
            self.logger.info("All of the detected database containers have volumes attached")
            return CheckerResult.PASSED
        else:
            return CheckerResult.FAILED

    def __is_volume_attached(self, container: Container):
        return len(container.attrs.get('Mounts')) > 0

    def __is_container_a_db_container(self, container: Container) -> bool:
        database_processes = ['redis-server', 'postgres', 'mongod', 'mysqld', 'mariadbd', 'influxd', 'neo4j', 'asd',
                              'couchdb', 'rethinkdb', 'couchbase', 'orientdb', 'arangod', 'cockroach', 'db2']
        processes = container.top().get('Processes')
        for process in processes:
            for db_process in database_processes:
                if db_process in process[-1]:
                    return True
        return False
