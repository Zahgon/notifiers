from __future__ import annotations

import json
import logging

import requests

log = logging.getLogger("notifiers")


class RequestsHelper:
    """A wrapper around :class:`requests.Session` which enables generically handling HTTP requests"""

    @classmethod
    def request(
        self,
        url: str,
        method: str,
        raise_for_status: bool = True,
        path_to_errors: tuple | None = None,
        *args,
        **kwargs,
    ) -> tuple:
        """
        A wrapper method for :meth:`~requests.Session.request``, which adds some defaults and logging

        :param url: The URL to send the reply to
        :param method: The method to use
        :param raise_for_status: Should an exception be raised for a failed response. Default is **True**
        :param args: Additional args to be sent to the request
        :param kwargs: Additional args to be sent to the request
        :return: Dict of response body or original :class:`requests.Response`
        """
        pass


def get(url: str, *args, **kwargs) -> tuple:
    """Send a GET request. Returns a dict or :class:`requests.Response <Response>`"""
    pass


def post(url: str, *args, **kwargs) -> tuple:
    """Send a POST request. Returns a dict or :class:`requests.Response <Response>`"""
    pass


def file_list_for_request(list_of_paths: list, key_name: str, mimetype: str | None = None) -> list:
    """
    Convenience function to construct a list of files for multiple files upload by :mod:`requests`

    :param list_of_paths: Lists of strings to include in files. Should be pre validated for correctness
    :param key_name: The key name to use for the file list in the request
    :param mimetype: If specified, will be included in the requests
    :return: List of open files ready to be used in a request
    """
    pass
