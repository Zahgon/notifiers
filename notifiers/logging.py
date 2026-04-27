from __future__ import annotations

import copy
import logging
import sys

import notifiers
from notifiers.exceptions import NotifierException


class NotificationHandler(logging.Handler):
    """A :class:`logging.Handler` that enables directly sending log messages to notifiers"""

    def __init__(self, provider: str, defaults: dict | None = None, **kwargs):
        """
        Sets ups the handler

        :param provider: Provider name to use
        :param defaults: Default provider data to use. Can fallback to environs
        :param kwargs: Additional kwargs
        """
        self.defaults = defaults or {}
        self.provider = None
        self.fallback = None
        self.fallback_defaults = None
        self.init_providers(provider, kwargs)
        super().__init__(**kwargs)

    def init_providers(self, provider, kwargs):
        """
        Inits main and fallback provider if relevant

        :param provider: Provider name to use
        :param kwargs: Additional kwargs
        :raises ValueError: If provider name or fallback names are not valid providers, a :exc:`ValueError` will
         be raised
        """
        pass

    def emit(self, record):
        """
        Override the :meth:`~logging.Handler.emit` method that takes the ``msg`` attribute from the log record passed

        :param record: :class:`logging.LogRecord`
        """
        pass

    def __repr__(self):
        level = logging.getLevelName(self.level)
        name = self.provider.name
        return f"<{self.__class__.__name__} {name}({level})>"

    def handleError(self, record):
        """
        Handles any errors raised during the :meth:`emit` method. Will only try to pass exceptions to fallback notifier
        (if defined) in case the exception is a sub-class of :exc:`~notifiers.exceptions.NotifierException`

        :param record: :class:`logging.LogRecord`
        """
        pass
