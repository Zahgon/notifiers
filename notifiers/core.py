from __future__ import annotations

import importlib.machinery
import importlib.util
import logging
from abc import ABC, abstractmethod

try:
    import jsonschema
    from jsonschema.exceptions import best_match
except ImportError:
    jsonschema = None  # type: ignore[assignment]
    best_match = None  # type: ignore[assignment]

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

try:
    from importlib_metadata import entry_points
except ImportError:
    entry_points = None  # type: ignore[assignment]

from .exceptions import BadArguments, NoSuchNotifierError, NotificationError, SchemaError
from .utils.helpers import dict_from_environs, merge_dicts
from .utils.schema.formats import format_checker

DEFAULT_ENVIRON_PREFIX = "NOTIFIERS_"

log = logging.getLogger("notifiers")

FAILURE_STATUS = "Failure"
SUCCESS_STATUS = "Success"


class Response:
    """
    A wrapper for the Notification response.

    :param status: Response status string. ``SUCCESS`` or ``FAILED``
    :param provider: Provider name that returned that response. Correlates to :attr:`~notifiers.core.Provider.name`
    :param data: The notification data that was used for the notification
    :param response: The response object that was returned. Usually :class:`requests.Response`
    :param errors: Holds a list of errors if relevant
    """

    def __init__(
        self,
        status: str,
        provider: str,
        data: dict,
        response: requests.Response = None,
        errors: list | None = None,
    ):
        self.status = status
        self.provider = provider
        self.data = data
        self.response = response
        self.errors = errors

    def __repr__(self):
        return f"<Response,provider={self.provider.capitalize()},status={self.status}, errors={self.errors}>"

    def raise_on_errors(self):
        """
        Raises a :class:`~notifiers.exceptions.NotificationError` if response hold errors

        :raises: :class:`~notifiers.exceptions.NotificationError`: If response has errors
        """
        pass

    @property
    def ok(self):
        pass


class SchemaResource(ABC):
    """Base class that represent an object schema and its utility methods"""

    @property
    @abstractmethod
    def _required(self) -> dict:
        """Will hold the schema's required part"""

    @property
    @abstractmethod
    def _schema(self) -> dict:
        """Resource JSON schema without the required part"""

    _merged_schema = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Resource provider name"""

    @property
    def schema(self) -> dict:
        """
        A property method that'll return the constructed provider schema.
        Schema MUST be an object and this method must be overridden

        :return: JSON schema of the provider
        """
        pass

    @property
    def arguments(self) -> dict:
        """Returns all the provider argument as declared in the JSON schema"""
        pass

    @property
    def required(self) -> dict:
        """Returns a dict of the relevant required parts of the schema"""
        pass

    @property
    def defaults(self) -> dict:
        """A dict of default provider values if such is needed"""
        pass

    def create_response(
        self,
        data: dict | None = None,
        response: requests.Response = None,
        errors: list | None = None,
    ) -> Response:
        """
        Helper function to generate a :class:`~notifiers.core.Response` object

        :param data: The data that was used to send the notification
        :param response: :class:`requests.Response` if exist
        :param errors: List of errors if relevant
        """
        pass

    def _merge_defaults(self, data: dict) -> dict:
        """
        Convenience method that calls :func:`~notifiers.utils.helpers.merge_dicts` in order to merge
        default values

        :param data: Notification data
        :return: A merged dict of provided data with added defaults
        """
        pass

    def _get_environs(self, prefix: str | None = None) -> dict:
        """
        Fetches set environment variables if such exist, via the :func:`~notifiers.utils.helpers.dict_from_environs`
        Searches for `[PREFIX_NAME]_[PROVIDER_NAME]_[ARGUMENT]` for each of the arguments defined in the schema

        :param prefix: The environ prefix to use. If not supplied, uses the default
        :return: A dict of arguments and value retrieved from environs
        """
        pass

    def _prepare_data(self, data: dict) -> dict:
        """
        Use this method to manipulate data that'll fit the respected provider API.
         For example, all provider must use the ``message`` argument but sometimes provider expects a different
         variable name for this, like ``text``.

        :param data: Notification data
        :return: Returns manipulated data, if there's a need for such manipulations.
        """
        pass

    def _validate_schema(self):
        """
        Validates provider schema for syntax issues. Raises :class:`~notifiers.exceptions.SchemaError` if relevant

        :raises: :class:`~notifiers.exceptions.SchemaError`
        """
        pass

    def _validate_data(self, data: dict):
        """
        Validates data against provider schema. Raises :class:`~notifiers.exceptions.BadArguments` if relevant

        :param data: Data to validate
        :raises: :class:`~notifiers.exceptions.BadArguments`
        """
        pass

    def _validate_data_dependencies(self, data: dict) -> dict:
        """
        Validates specific dependencies based on the content of the data, as opposed to its structure which can be
        verified on the schema level

        :param data: Data to validate
        :return: Return data if its valid
        :raises: :class:`~notifiers.exceptions.NotifierException`
        """
        pass

    def _process_data(self, **data) -> dict:
        """
        The main method that process all resources data. Validates schema, gets environs, validates data, prepares
         it via provider requirements, merges defaults and check for data dependencies

        :param data: The raw data passed by the notifiers client
        :return: Processed data
        """
        pass

    def __init__(self):
        pass


class Provider(SchemaResource, ABC):
    """The Base class all notification providers inherit from."""

    _resources = {}

    def __repr__(self):
        return f"<Provider:[{self.name.capitalize()}]>"

    def __getattr__(self, item):
        if item in self._resources:
            return self._resources[item]
        raise AttributeError(f"{self} does not have a property {item}")

    @property
    @abstractmethod
    def base_url(self):
        pass

    @property
    @abstractmethod
    def site_url(self):
        pass

    @property
    def metadata(self) -> dict:
        """
        Returns a dict of the provider metadata as declared. Override if needed.
        """
        pass

    @property
    def resources(self) -> list:
        """Return a list of names of relevant :class:`~notifiers.core.ProviderResource` objects"""
        pass

    @abstractmethod
    def _send_notification(self, data: dict) -> Response:
        """
        The core method to trigger the provider notification. Must be overridden.

        :param data: Notification data
        """

    def notify(self, raise_on_errors: bool = False, **kwargs) -> Response:
        """
        The main method to send notifications. Prepares the data via the
        :meth:`~notifiers.core.SchemaResource._prepare_data` method and then sends the notification
        via the :meth:`~notifiers.core.Provider._send_notification` method

        :param kwargs: Notification data
        :param raise_on_errors: Should the :meth:`~notifiers.core.Response.raise_on_errors` be invoked immediately
        :return: A :class:`~notifiers.core.Response` object
        :raises: :class:`~notifiers.exceptions.NotificationError` if ``raise_on_errors`` is set to True and response
         contained errors
        """
        pass


class ProviderResource(SchemaResource, ABC):
    """The base class that is used to fetch provider related resources like rooms, channels, users etc."""

    @property
    @abstractmethod
    def resource_name(self):
        pass

    @abstractmethod
    def _get_resource(self, data: dict):
        pass

    def __call__(self, **kwargs):
        data = self._process_data(**kwargs)
        return self._get_resource(data)

    def __repr__(self):
        return f"<ProviderResource,provider={self.name},resource={self.resource_name}>"


# Avoid premature import
try:
    from .providers import _all_providers  # noqa: E402
except (ImportError, AttributeError):
    _all_providers = {}  # type: ignore[assignment]


def get_notifier(provider_name: str, strict: bool = False) -> Provider:
    """
    Convenience method to return an instantiated :class:`~notifiers.core.Provider` object according to it ``name``

    :param provider_name: The ``name`` of the requested :class:`~notifiers.core.Provider`
    :param strict: Raises a :class:`ValueError` if the given provider string was not found
    :return: :class:`Provider` or None
    :raises ValueError: In case ``strict`` is True and provider not found
    """
    pass


def load_provider_from_points(entry_points: str) -> Provider:
    """Load a Provider class from a given entry point string.

    This function takes an entry point string in the format
    'module_path:class_name' and dynamically imports the specified Provider class.
    It performs validation to ensure the loaded class is a valid Provider.

    :param entry_points: A string in the format 'module_path:class_name' (e.g. 'myapp.providers:EmailProvider')
    :return: :class:`Provider` The loaded Provider class
    :raises ValueError: If the entry_points string format is invalid
    :raises ImportError: If the specified module cannot be imported
    :raises AttributeError: If the specified class cannot be found in the module
    :raises TypeError: If the loaded class is not a subclass of Provider

    Example:
        >>> entry_points = "myapp.providers:EmailProvider"
        >>> provider_class = load_provider_from_points(entry_points)
        >>> provider = provider_class()
    """
    pass


def get_providers_from_entry_points(group_name: str = "notifiers") -> dict:
    """
    Get a dictionary of plugins from the entry points based on the given group name.

    This function will search for the entry points with the specified group name
    and return a dictionary where the keys are the names of the entry points and
    the values are the corresponding entry point values.

    :param group_name: The group name of the entry points to search for.
    :return: Dict: A dictionary containing the entry point names as keys and their corresponding values as values.

    Example:
        >>> get_providers_from_entry_points("notifiers")
        {"plugin1": "package.module:PluginClass", "plugin2": "package2.module:OtherPluginClass"}
    """
    pass


def get_all_providers() -> dict:
    """Get all providers from the entry points and the default providers.

    :return: Dict: A dictionary containing the entry point names as keys and their corresponding values as values.

    """
    pass


def all_providers() -> list:
    """Returns a list of all :class:`~notifiers.core.Provider` names"""
    pass


def notify(provider_name: str, **kwargs) -> Response:
    """
    Quickly sends a notification without needing to get a notifier via the :func:`get_notifier` method.

    :param provider_name: Name of the notifier to use. Note that if this notifier name does not exist it will raise a
    :param kwargs: Notification data, dependant on provider
    :return: :class:`Response`
    :raises: :class:`~notifiers.exceptions.NoSuchNotifierError` If ``provider_name`` is unknown,
     will raise notification error
    """
    pass
