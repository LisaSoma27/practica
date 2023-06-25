import yaml


def read_config():
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except (FileNotFoundError, OSError) as e:
        print(e)


def write_config(config):
    try:
        with open('config.yaml', 'w') as file:
            yaml.safe_dump(config, file, sort_keys=False)
    except(FileNotFoundError, OSError) as e:
        print(e)
