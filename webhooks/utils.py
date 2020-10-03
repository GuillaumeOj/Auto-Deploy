from hmac import HMAC
from hmac import compare_digest

from webhooks import app


def verify_signature(received_signature, payload):
    secret_key = app.config["GIT_HUB_WEBHOOK_TOKEN"].encode()
    excepted_signature = HMAC(secret_key, payload, "sha1").hexdigest()

    return compare_digest(excepted_signature, received_signature)
