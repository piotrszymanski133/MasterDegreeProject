from docker.models.containers import Container


class DatabaseContainerDetector:
    def is_container_a_db_container(self, container: Container) -> bool:
        return self.__is_redis(container) or self.__is_postgres(container) or self.__is_mongo(container) or \
               self.__is_mysql(container) or self.__is_mariadb(container) or self.__is_influxdb(container) or \
               self.__is_percona(container) or self.__is_neo4j(container) or self.__is_cassandra(container) or \
               self.__is_couchdb(container) or self.__is_rethinkdb(container) or self.__is_couchbase(container) or \
               self.__is_crate(container) or self.__is_aerospike(container) or self.__is_orientdb(container) or \
               self.__is_arangodb(container) or self.__is_cockroach(container) or self.__is_db2(container)

    def __is_redis(self, container: Container):
        return False

    def __is_postgres(self, container: Container):
        return False

    def __is_mongo(self, container: Container):
        return False

    def __is_mysql(self, container: Container):
        return False

    def __is_mariadb(self, container: Container):
        return False

    def __is_influxdb(self, container: Container):
        return False

    def __is_percona(self, container: Container):
        return False

    def __is_neo4j(self, container: Container):
        return False

    def __is_cassandra(self, container: Container):
        return False

    def __is_couchdb(self, container: Container):
        return False

    def __is_rethinkdb(self, container: Container):
        return False

    def __is_couchbase(self, container: Container):
        return False

    def __is_crate(self, container: Container):
        return False

    def __is_aerospike(self, container: Container):
        return False

    def __is_orientdb(self, container: Container):
        return False

    def __is_arangodb(self, container: Container):
        return False

    def __is_cockroach(self, container: Container):
        return False

    def __is_db2(self, container: Container):
        return False