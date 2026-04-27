import logging
import os
from pathlib import Path

log = logging.getLogger("notifiers")


def text_to_bool(value: str) -> bool:
    """
    Tries to convert a text value to a bool. If unsuccessful returns if value is None or not

    :param value: Value to check
    """
    pass


def merge_dicts(target_dict: dict, merge_dict: dict) -> dict:
    """
    Merges ``merge_dict`` into ``target_dict`` if the latter does not already contain a value for each of the key
    names in ``merge_dict``. Used to cleanly merge default and environ data into notification payload.

    :param target_dict: The target dict to merge into and return, the user provided data for example
    :param merge_dict: The data that should be merged into the target data
    :return: A dict of merged data
    """
    pass


def dict_from_environs(prefix: str, name: str, args: list) -> dict:
    """
    Return a dict of environment variables correlating to the arguments list, main name and prefix like so:
    [prefix]_[name]_[arg]

    :param prefix: The environ prefix to use
    :param name: Main part
    :param args: List of args to iterate over
    :return: A dict of found environ values
    """
    pass


def snake_to_camel_case(value: str) -> str:
    """
    Convert a snake case param to CamelCase

    :param value: The value to convert
    :return: A CamelCase value
    """
    pass


def valid_file(path: str) -> bool:
    """
    Verifies that a string path actually exists and is a file

    :param path: The path to verify
    :return: **True** if path exist and is a file
    """
    pass
