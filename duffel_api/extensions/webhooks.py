import hmac
import hashlib
import base64


class WebhooksValidator:
    @staticmethod
    def signature(secret, payload, timestamp):
        """Generate a new signature from a secret and timestamp for a payload.
        This is used to verify a received notification.
        """
        # We need the signed payload as bytes
        signed_payload = timestamp.encode() + b"." + payload
        # The signature in bytes
        signature = hmac.new(secret, signed_payload, hashlib.sha256).digest()
        # Base16 encode the signature, in lowercase, then decode to a string
        return base64.b16encode(signature).lower().decode()

    @staticmethod
    def compare(secret, request):
        """Compare the request's payload with our secret to verify that it was
        sent from Duffel, and not from a malicious actor.

        """
        # Get the payload as bytes so that we can construct the signature from
        # raw/unparsed data
        raw_payload = request.get_data()

        # Format:
        # t=1616202842,v1=8aebaa7ecaf36950721e4321b6a56d7493d13e73814de672ac5ce4ddd7435054
        raw_signature = request.headers['X-Duffel-Signature']
        pairs = list(map(lambda x: x.split('='), raw_signature.split(',')))
        t = pairs[0][1]
        v1 = pairs[1][1]

        # Recreate the signature
        local_signature = signature(secret, raw_payload, t)

        return hmac.compare_digest(v1, local_signature)
