from hmac import HMAC
from hmac import compare_digest

from webhooks import app


class WrongSignatureType(BaseException):
    pass


class NoSignature(BaseException):
    pass


class WrongDigestMode(BaseException):
    pass


def verify_signature(request):
    payload = request.data
    headers = request.headers

    secret_key = app.config["GIT_HUB_WEBHOOK_TOKEN"].encode()

    if "X-Hub-Signature" in headers:
        signature_header = headers["X-Hub-Signature"]
        if "=" in signature_header:
            sha_name, received_signature = signature_header.split("=")
        else:
            raise WrongSignatureType()
    else:
        raise NoSignature()

    if sha_name != "sha1":
        raise WrongDigestMode()

    excepted_signature = HMAC(secret_key, payload, "sha1").hexdigest()

    return compare_digest(excepted_signature, received_signature)
