from ..core import Provider, Response
from ..utils import requests


class SimplePush(Provider):
    """Send SimplePush notifications"""

    base_url = "https://api.simplepush.io/send"
    site_url = "https://simplepush.io/"
    name = "simplepush"

    _required = {"required": ["key", "message"]}
    _schema = {
        "type": "object",
        "properties": {
            "key": {"type": "string", "title": "your user key"},
            "message": {"type": "string", "title": "your message"},
            "title": {"type": "string", "title": "message title"},
            "event": {"type": "string", "title": "Event ID"},
        },
        "additionalProperties": False,
    }

    def _prepare_data(self, data: dict) -> dict:
        pass

    def _send_notification(self, data: dict) -> Response:
        pass
