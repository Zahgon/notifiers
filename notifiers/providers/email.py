from __future__ import annotations

import mimetypes
import smtplib
import socket
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path
from smtplib import SMTPAuthenticationError, SMTPSenderRefused, SMTPServerDisconnected

from ..core import Provider, Response
from ..utils.schema.helpers import list_to_commas, one_or_more

DEFAULT_SUBJECT = "New email from 'notifiers'!"
DEFAULT_FROM = f"notifiers@{socket.getfqdn()}"
DEFAULT_SMTP_HOST = "localhost"


class SMTP(Provider):
    """Send emails via SMTP"""

    base_url = None
    site_url = "https://en.wikipedia.org/wiki/Email"
    name = "email"

    _required = {"required": ["message", "to"]}

    _schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string", "title": "the content of the email message"},
            "subject": {"type": "string", "title": "the subject of the email message"},
            "to": one_or_more(
                {
                    "type": "string",
                    "format": "email",
                    "title": "one or more email addresses to use",
                }
            ),
            "cc": one_or_more(
                {
                    "type": "string",
                    "format": "email",
                    "title": "one or more email addresses to use",
                }
            ),
            "bcc": one_or_more(
                {
                    "type": "string",
                    "format": "email",
                    "title": "one or more email addresses to use",
                }
            ),
            "from": {
                "type": "string",
                "format": "email",
                "title": "the FROM address to use in the email",
            },
            "from_": {
                "type": "string",
                "format": "email",
                "title": "the FROM address to use in the email",
                "duplicate": True,
            },
            "attachments": one_or_more(
                {
                    "type": "string",
                    "format": "valid_file",
                    "title": "one or more attachments to use in the email",
                }
            ),
            "host": {
                "type": "string",
                "format": "hostname",
                "title": "the host of the SMTP server",
            },
            "port": {
                "type": "integer",
                "format": "port",
                "title": "the port number to use",
            },
            "username": {"type": "string", "title": "username if relevant"},
            "password": {"type": "string", "title": "password if relevant"},
            "tls": {"type": "boolean", "title": "should TLS be used"},
            "ssl": {"type": "boolean", "title": "should SSL be used"},
            "html": {
                "type": "boolean",
                "title": "should the email be parse as an HTML file",
            },
            "login": {"type": "boolean", "title": "Trigger login to server"},
        },
        "dependencies": {
            "username": ["password"],
            "password": ["username"],
            "ssl": ["tls"],
        },
        "additionalProperties": False,
    }

    @staticmethod
    def _get_mimetype(attachment: Path) -> tuple[str, str]:
        """Taken from https://docs.python.org/3/library/email.examples.html"""
        pass

    def __init__(self):
        super().__init__()
        self.smtp_server = None
        self.configuration = None

    @property
    def defaults(self) -> dict:
        pass

    def _prepare_data(self, data: dict) -> dict:
        pass

    @staticmethod
    def _build_email(data: dict) -> EmailMessage:
        pass

    def _add_attachments(self, attachments: list[str], email: EmailMessage):
        pass

    def _connect_to_server(self, data: dict):
        pass

    @staticmethod
    def _get_configuration(data: dict) -> tuple:
        pass

    def _send_notification(self, data: dict) -> Response:
        pass
