FAKE_CONTAINER_ID = '81cf499cc928ce3fedc250a080d2b9b978df20e4517304c45211e8a68b33e254'
INVALID_MAX_RETRY_COUNT = 22

valid_container_config = {
    'Id': FAKE_CONTAINER_ID,
    'Config': {'Privileged': False, 'Tty': False},
    'Image': 'busybox:latest',
    'Name': 'foobar',
    "State": {
        "Status": "running",
        "Running": True,
        "Pid": 0,
        "ExitCode": 0,
        "StartedAt": "2013-09-25T14:01:18.869545111+02:00",
        "Ghost": False
    },
    "HostConfig": {
        "RestartPolicy": {
            "Name": "on-failure",
            "MaximumRetryCount": 5
        },
        "LogConfig": {
            "Type": "json-file",
            "Config": {}
        }
    },
    "MacAddress": "02:42:ac:11:00:0a"
}

container_config_invalid_restart_policy = {
    'Id': FAKE_CONTAINER_ID,
    'Config': {'Privileged': False, 'Tty': False},
    'Image': 'busybox:latest',
    'Name': 'foobar',
    "State": {
        "Status": "running",
        "Running": True,
        "Pid": 0,
        "ExitCode": 0,
        "StartedAt": "2013-09-25T14:01:18.869545111+02:00",
        "Ghost": False
    },
    "HostConfig": {
        "RestartPolicy": {
            "Name": "always",
            "MaximumRetryCount": 5
        },
        "LogConfig": {
            "Type": "json-file",
            "Config": {}
        }
    },
    "MacAddress": "02:42:ac:11:00:0a"
}

container_config_invalid_max_retry_count = {
    'Id': FAKE_CONTAINER_ID,
    'Config': {'Privileged': False, 'Tty': False},
    'Image': 'busybox:latest',
    'Name': 'foobar',
    "State": {
        "Status": "running",
        "Running": True,
        "Pid": 0,
        "ExitCode": 0,
        "StartedAt": "2013-09-25T14:01:18.869545111+02:00",
        "Ghost": False
    },
    "HostConfig": {
        "RestartPolicy": {
            "Name": "on-failure",
            "MaximumRetryCount": INVALID_MAX_RETRY_COUNT
        },
        "LogConfig": {
            "Type": "json-file",
            "Config": {}
        }
    },
    "MacAddress": "02:42:ac:11:00:0a"
}

