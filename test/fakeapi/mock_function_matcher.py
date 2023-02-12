from test.fakeapi import fake_api


def match_mock_function(mock_attribute: str, function_params: dict):
    match mock_attribute:
        case 'containers.return_value':
            return fake_api.get_fake_containers(function_params)[1]
        case 'inspect_container.return_value':
            return fake_api.get_fake_inspect_container(function_params)[1]
        case 'volumes.return_value':
            return fake_api.get_fake_volume_list(function_params)[1]

    """
mock_attrs = {
        'build.return_value': fake_api.FAKE_IMAGE_ID,
        'commit.return_value': fake_api.post_fake_commit()[1],
        'create_container.return_value':
            fake_api.post_fake_create_container()[1],
        'create_host_config.side_effect': api_client.create_host_config,
        'create_network.return_value': fake_api.post_fake_network()[1],
        'create_secret.return_value': fake_api.post_fake_secret()[1],
        'exec_create.return_value': fake_api.post_fake_exec_create()[1],
        'exec_start.return_value': fake_api.post_fake_exec_start()[1],
        'images.return_value': fake_api.get_fake_images()[1],
        ,
        'inspect_image.return_value': fake_api.get_fake_inspect_image()[1],
        'inspect_network.return_value': fake_api.get_fake_network()[1],
        'logs.return_value': [b'hello world\n'],
        'networks.return_value': fake_api.get_fake_network_list()[1],
        'start.return_value': None,
        'wait.return_value': {'StatusCode': 0},
        'version.return_value': fake_api.get_fake_version()
    }"""