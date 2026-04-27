from ..core import Provider, Response
from ..exceptions import NotifierException
from ..utils import requests


class Zulip(Provider):
    """Send Zulip notifications"""

    name = "zulip"
    site_url = "https://zulipchat.com/api/"
    api_endpoint = "/api/v1/messages"
    base_url = "https://{domain}.zulipchat.com"
    path_to_errors = ("msg",)

    __type = {
        "type": "string",
        "enum": ["stream", "private"],
        "title": "Type of message to send",
    }
    _required = {
        "allOf": [
            {"required": ["message", "email", "api_key", "to"]},
            {
                "oneOf": [{"required": ["domain"]}, {"required": ["server"]}],
                "error_oneOf": "Only one of 'domain' or 'server' is allowed",
            },
        ]
    }

    _schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string", "title": "Message content"},
            "email": {"type": "string", "format": "email", "title": "User email"},
            "api_key": {"type": "string", "title": "User API Key"},
            "type": __type,
            "type_": __type,
            "to": {"type": "string", "title": "Target of the message"},
            "subject": {
                "type": "string",
                "title": "Title of the stream message. Required when using stream.",
            },
            "domain": {"type": "string", "minLength": 1, "title": "Zulip cloud domain"},
            "server": {
                "type": "string",
                "format": "uri",
                "title": "Zulip server URL. Example: https://myzulip.server.com",
            },
        },
        "additionalProperties": False,
    }

    @property
    def defaults(self) -> dict:
        pass

    def _prepare_data(self, data: dict) -> dict:
        pass

    def _validate_data_dependencies(self, data: dict) -> dict:
        pass

    def _send_notification(self, data: dict) -> Response:
        pass
