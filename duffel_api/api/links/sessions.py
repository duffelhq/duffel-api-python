from typing import Optional

from ...http_client import HttpClient
from ...models import Session


class LinksSessionClient(HttpClient):
    def __init__(self, **kwargs):
        self._url = "/links/sessions"
        super().__init__(**kwargs)

    def create(self):
        return LinksSessionCreate(self)


class LinksSessionCreate(object):
    """Auxiliary class to provide methods for session request creation related data."""

    _reference: str
    _success_url: str
    _failure_url: str
    _abandonment_url: str
    _logo_url: Optional[str]
    _primary_color: Optional[str]
    _secondary_color: Optional[str]
    _checkout_display_text: Optional[str]
    _traveller_currency: Optional[str]
    _markup_amount: Optional[str]
    _markup_currency: Optional[str]
    _markup_rate: Optional[str]

    def __init__(self, client):
        self._client = client
        self._reference = ""
        self._success_url = ""
        self._failure_url = ""
        self._abandonment_url = ""
        self._logo_url = None
        self._primary_color = None
        self._secondary_color = None
        self._checkout_display_text = None
        self._traveller_currency = None
        self._markup_amount = None
        self._markup_currency = None
        self._markup_rate = None

    def reference(self, reference: str):
        """Way to identify the Session.

        This can be a user ID, or similar, and can be
        used to reconcile the Session with your internal systems.

        Example: "user_123"

        """
        self._reference = reference
        return self

    def success_url(self, success_url: str):
        """URL the traveller will be redirected to once an order has been created.

        Where the traveller will end up when their orders has been successfully created
        and they press the 'Return' button.

        Example: "https://example.com/success"

        """
        self._success_url = success_url
        return self

    def failure_url(self, failure_url: str):
        """URL the traveller will be redirected to if there is a failure.

        This is only applicable to a failure that can not be mitigated.

        Example: "https://example.com/failure"

        """
        self._failure_url = failure_url
        return self

    def abandonment_url(self, abandonment_url: str):
        """URL the traveller will be redirected to if they decide to abandon the session.

        This happens when the users presses the 'Return' button.

        Example: "https://example.com/abandonment"

        """
        self._abandonment_url = abandonment_url
        return self

    def logo_url(self, logo_url: str):
        """URL to the logo that will appear at the top-left corner.

        If not provided, Duffel's logo will be used. The logo provided will be resized to
        be 16 pixels high, to ensure it fits the header. The aspect ratio will be
        maintained, ensuring it won't look squashed or have misproportioned.

        Example: "https://example.com/logo.svg"

        """
        self._logo_url = logo_url
        return self

    def primary_color(self, primary_color: str):
        """Primary colour that will be used to customise the session.

        It should be an hexadecimal CSS-compatible colour. If one is not provided the
        default Duffel colour will be used.

        Example: "#000000"

        """
        self._primary_color = primary_color
        return self

    def secondary_color(self, secondary_color: str):
        """Secondary colour that will be used to customise the session.

        It should be an hexadecimal CSS-compatible colour. If one is not provided the
        default Duffel colour will be used.

        Example: "#000000"

        """
        self._secondary_color = secondary_color
        return self

    def checkout_display_text(self, checkout_display_text: str):
        """Text that will appear at the bottom of the checkout form.

        If not provided nothing will be displayed.

        Example: "Thank you for booking with us."

        """
        self._checkout_display_text = checkout_display_text
        return self

    def traveller_currency(self, traveller_currency: str):
        """The currency in which the traveller will see prices and pay in. If not provided
        it will default to the settlement currency of your account. The traveller will be
        able to change this currency before searching.

        Example: "GBP"

        """
        self._traveller_currency = traveller_currency
        return self

    def markup_amount(self, markup_amount: str):
        """The absolute amount that will be added to the final price to be paid by the
        traveller. If not provided it will default to zero. This field is required if
        markup_currency is provided.

        Example: "1.00"

        """
        self._markup_amount = markup_amount
        return self

    def markup_currency(self, markup_currency: str):
        """The currency of the markup_amount. It should always match the settlement
        currency of the organisation. This field is required is markup_amount is provided.

        Example: "GBP"

        """
        self._markup_currency = markup_currency
        return self

    def markup_rate(self, markup_rate: str):
        """The rate that will be applied to the total amount to be paid by the
        traveller. For a 1% markup provide 0.01 as the markup_rate. If not provided it
        will default to zero.

        Example: "0.01"

        """
        self._markup_rate = markup_rate
        return self

    class InvalidMandatoryFields(Exception):
        """Fields 'reference', 'success_url', 'failure_url', and 'abandonment_url' are
        mandatory"""

    class InvalidMarkup(Exception):
        """Both fields 'markup_amount' and 'markup_currency' have to exist or not at all
        but it is not possible to have one and not the other"""

    def _validate_mandatory(self):
        if (
            self._reference == ""
            or self._success_url == ""
            or self._failure_url == ""
            or self._abandonment_url == ""
        ):
            raise LinksSessionCreate.InvalidMandatoryFields

    def _validate_markup(self):
        if (self._markup_currency is None and self._markup_amount is not None) or (
            self._markup_currency is not None and self._markup_amount is None
        ):
            raise LinksSessionCreate.InvalidMarkup

    def execute(self):
        """POST /links/sessions - trigger the call to create the session"""
        self._validate_mandatory()

        body_data = {
            "reference": self._reference,
            "success_url": self._success_url,
            "failure_url": self._failure_url,
            "abandonment_url": self._abandonment_url,
        }

        if self._logo_url:
            body_data["logo_url"] = self._logo_url
        if self._primary_color:
            body_data["primary_color"] = self._primary_color
        if self._secondary_color:
            body_data["secondary_color"] = self._secondary_color
        if self._checkout_display_text:
            body_data["checkout_display_text"] = self._checkout_display_text
        if self._traveller_currency:
            body_data["traveller_currency"] = self._traveller_currency
        if self._markup_rate:
            body_data["markup_rate"] = self._markup_rate
        if self._markup_currency and self._markup_amount:
            body_data["markup_currency"] = self._markup_currency
            body_data["markup_amount"] = self._markup_amount
        else:
            self._validate_markup()

        res = self._client.do_post(self._client._url, body={"data": body_data})
        return Session.from_json(res["data"])
