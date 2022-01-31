from ...http_client import HttpClient
from ...models import Webhook


class WebhookClient(HttpClient):
    """Client to interact with Webhooks

    **Preview**

    This is not yet finalised. It may change or be removed or be not yet
    accessible. This documentation is designed to give you an idea of features
    we'll be adding to our API in the future."""

    def __init__(self, **kwargs):
        self._url = "/air/webhooks"
        super().__init__(**kwargs)

    def create(self):
        """Initiate creation of a Webhook"""
        return WebhookCreate(self)

    def update(self, id_):
        """Initiate updating of a Webhook"""
        return WebhookUpdate(self, id_)

    def ping(self, id_):
        """Ping a webhook.

        Send a ping, a "fake event" notification, to a webhook.
        """
        url = f"{self._url}/{id_}/actions/ping"
        self.do_post(url)
        return None


class WebhookCreate(object):
    """Auxiliary class to provide methods for webhook creating related data"""

    def __init__(self, client):
        self._client = client

    def events(self, events):
        """Add events"""
        self._events = events
        return self

    def url(self, url):
        """Add URL"""
        self._url = url
        return self

    def execute(self):
        """POST /air/webhooks"""
        res = self._client.do_post(
            self._client._url,
            body={"data": {"events": self._events, "url": self._url}},
        )
        return Webhook.from_json(res["data"])


class WebhookUpdate(object):
    """Auxiliary class to provide methods for webhook updating related data"""

    def __init__(self, client, id):
        self._client = client
        self._id = id

    def active(self, active):
        """Set webhook to active"""
        self._active = active
        return self

    def execute(self):
        """PATCH /air/webhooks/{id}"""
        url = f"{self._client._url}/{self._id}"

        res = self._client.do_patch(
            url,
            body={"data": {"active": self._active}},
        )

        return Webhook.from_json(res["data"])
