from dataclasses import dataclass


@dataclass
class Session:
    """A Session represents the traveller's session as they go through the search and book
    flow to create an order.

    You should create a Session every time a user wishes to go through the search and book
    flow.

    Once an order has been created as part of a Session it will no longer be usable to
    create an order.

    Each Session is valid for 20 minutes after it is first used, and can be used up to 1
    hour after it is created.
    """

    # The URL to the search and book Session. Redirect travellers to this URL to take them
    # to Links. If you’re using a custom subdomain, the URL will use your
    # subdomain. Otherwise, it’ll use links.duffel.com.
    #
    # Example: "https://links.duffel.com?token=U0ZNeU5UWS5nMmdEYlFBQUFCWXdNREF3TESTWU5rNWxPWGR1VDNoUFYydEdiMVZEYmdZQXB5M0RPb1lCWWdBQlVZQS5aTESTRHYwdmVyQl9vbkJ5TESTNHVsSGdIZjFiaGctY0tmdVdITESTNVlv" # noqa: E501
    url: str

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(url=json["url"])
