import json
import os

from flask import Response

from webhooks.utils import verify_signature


APP_DIR = os.path.dirname(os.path.abspath(__name__))


class TestUtils:
    data_path = os.path.join(APP_DIR, "tests", "events", "push_event.json")

    with open(data_path, "r") as f:
        payload = json.load(f)

    data = json.dumps(payload, separators=(",", ":")).encode()

    def test_verify_signature(self, client):
        github_signature = "9296374267ad49bd3fb54cdbfb129da7f4009883"
        headers = {"X-Hub-Signature": f"sha1={github_signature}"}

        request = Response(
            response=self.data, headers=headers, mimetype="application/json"
        )

        assert verify_signature(request)

    def test_verify_signature_with_wrong_signature(self, client):
        github_signature = "foo"
        headers = {"X-Hub-Signature": f"sha1={github_signature}"}

        request = Response(
            response=self.data, headers=headers, mimetype="application/json"
        )

        assert not verify_signature(request)

    def test_verify_signature_with_wrong_payload(self, client):
        data = json.dumps({"foo": "bar"}, separators=(",", ":")).encode()

        github_signature = "9296374267ad49bd3fb54cdbfb129da7f4009883"
        headers = {"X-Hub-Signature": f"sha1={github_signature}"}

        request = Response(response=data, headers=headers, mimetype="application/json")

        assert not verify_signature(request)
