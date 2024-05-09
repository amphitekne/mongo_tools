from .config_reader import config_files


def get_configuration(alias: str) -> dict:
    for filename, content in config_files.items():
        if content["alias"] == alias:
            return content
    print(f"Configuration file {alias} not found")
