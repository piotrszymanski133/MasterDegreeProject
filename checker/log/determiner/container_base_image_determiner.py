from docker.models.containers import Container


class ContainerBaseImageDeterminer:

    def determine_container_base_image(self, container: Container) -> str:
        return None