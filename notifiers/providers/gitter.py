from ..core import Provider, ProviderResource, Response
from ..exceptions import ResourceError
from ..utils import requests


class GitterMixin:
    """Shared attributes between :class:`~notifiers.providers.gitter.GitterRooms` and
    :class:`~notifiers.providers.gitter.Gitter`"""

    name = "gitter"
    path_to_errors = "errors", "error"
    base_url = "https://api.gitter.im/v1/rooms"

    def _get_headers(self, token: str) -> dict:
        """
        Builds Gitter requests header bases on the token provided

        :param token: App token
        :return: Authentication header dict
        """
        pass


class GitterRooms(GitterMixin, ProviderResource):
    """Returns a list of Gitter rooms via token"""

    resource_name = "rooms"

    _required = {"required": ["token"]}

    _schema = {
        "type": "object",
        "properties": {
            "token": {"type": "string", "title": "access token"},
            "filter": {"type": "string", "title": "Filter results"},
        },
        "additionalProperties": False,
    }

    def _get_resource(self, data: dict) -> list:
        pass


class Gitter(GitterMixin, Provider):
    """Send Gitter notifications"""

    message_url = "/{room_id}/chatMessages"
    site_url = "https://gitter.im"

    _resources = {"rooms": GitterRooms()}

    _required = {"required": ["message", "token", "room_id"]}
    _schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string", "title": "Body of the message"},
            "token": {"type": "string", "title": "access token"},
            "room_id": {
                "type": "string",
                "title": "ID of the room to send the notification to",
            },
        },
        "additionalProperties": False,
    }

    def _prepare_data(self, data: dict) -> dict:
        pass

    @property
    def metadata(self) -> dict:
        pass

    def _send_notification(self, data: dict) -> Response:
        pass
