import yaml


def get_excluded_checkers():
    config = read_config_file()
    excluded_checkers = config.get('excluded_checkers')
    return excluded_checkers if excluded_checkers is not None else []


def read_config_file():
    with open("config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)
