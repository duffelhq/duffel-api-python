from ..http_client import HttpClient
from ..models import Webhook


class WebhookClient(HttpClient):
    """Client to interact with Webhooks"""
    def __init__(self, **kwargs):
        self._url = "/air/webhooks"
        super().__init__(**kwargs)

    def create(self, url, events):
        """Create a new webhook"""
        res = self.do_post(self._url,
                           body={"data": {
                               "url": url,
                               "events": events
                           }})
        return Webhook(res["data"])

    def update(self, id_, active):
        """Update a webhook's active state"""
        res = self.do_patch("{}/{}".format(self._url, id_),
                            body={"data": {
                                "active": active
                            }})
        return Webhook(res["data"])

    def ping(self, id_):
        """Trigger a ping event for the webhook to be notified with"""
        self.do_post("{}/{}/actions/ping".format(self._url, id_), body={})
        # TODO(jesse-c): There's No-Content, but this could be nicer.
        return None
