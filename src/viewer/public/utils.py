import re
import shutil
from configparser import ConfigParser
from pathlib import Path


def get_config(section: str, key: str) -> str:
    """Get the config from config file.

    Args:
        section (str): The section in the config file
        key (str): The key in the section

    Returns:
        str: The configuration
    """
    curr_dir = Path(__file__).parent
    config_file_location = curr_dir.parent.parent.parent / "config.ini"

    cfg = ConfigParser()
    cfg.read(config_file_location)
    return cfg[section][key]


def get_temp_directory(
    folder: str, subfolder: str | None = None, reset: bool = False
) -> Path:
    """Create a temporary directory.

    Args:
        folder (str): The folder name
        subfolder (str | None, optional): The subfolder name. Defaults to None.
        reset (bool, optional): Whenever to delete files in the folder or subfolder
            if it exists. Defaults to False.

    Returns:
        Path: The path of the folder created
    """
    curr_dir = Path(__file__).parent
    temp_file_location = curr_dir.parent / "temp_files" / folder
    if subfolder is not None:
        temp_file_location = temp_file_location / subfolder
    if reset:
        shutil.rmtree(temp_file_location, ignore_errors=True)
    temp_file_location.mkdir(parents=True, exist_ok=True)
    return temp_file_location


def to_camel(snake: str) -> str:
    """Convert snake_case string to camelCase.

    Args:
        snake (str): The snake_case string.

    Returns:
        str: The camelCase string.
    """
    if re.match("^[a-z]+[A-Za-z0-9]*$", snake) and not re.search(r"\d[a-z]", snake):
        return snake

    camel = to_pascal(snake)
    return re.sub("(^_*[A-Z])", lambda x: x.group(1).lower(), camel)


def to_pascal(snake: str) -> str:
    """Convert snake_case string to PascalCase.

    Args:
        snake (str): The snake_case string.

    Returns:
        str: The PascalCase string.
    """
    camel = snake.title()
    return re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)
