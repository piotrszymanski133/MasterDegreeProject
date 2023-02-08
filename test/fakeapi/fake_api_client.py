import copy
import docker
from docker.constants import DEFAULT_DOCKER_API_VERSION
from unittest import mock
from .mock_function_matcher import match_mock_function


class CopyReturnMagicMock(mock.MagicMock):
    """
    A MagicMock which deep copies every return value.
    """
    def _mock_call(self, *args, **kwargs):
        ret = super()._mock_call(*args, **kwargs)
        if isinstance(ret, (dict, list)):
            ret = copy.deepcopy(ret)
        return ret


def make_fake_api_client(mock_attributes: dict, overrides=None):
    """
    Returns non-complete fake APIClient.
    This returns most of the default cases correctly, but most arguments that
    change behaviour will not work.
    """
    if overrides is None:
        overrides = {}
    mock_attrs = {}
    for attribute, parameters in mock_attributes.items():
        mock_attrs[attribute] = match_mock_function(attribute, parameters)

    mock_attrs['create_host_config.side_effect'] = docker.APIClient(version=DEFAULT_DOCKER_API_VERSION)\
        .create_host_config
    mock_attrs.update(overrides)
    mock_client = CopyReturnMagicMock(**mock_attrs)

    mock_client._version = docker.constants.DEFAULT_DOCKER_API_VERSION
    return mock_client


def make_fake_client(mock_attributes: dict, overrides=None):
    """
    Returns a Client with a fake APIClient.
    """
    client = docker.DockerClient(version=DEFAULT_DOCKER_API_VERSION)
    client.api = make_fake_api_client(mock_attributes, overrides)
    return client
