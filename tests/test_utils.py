import json
import os

from webhooks.utils import verify_signature


APP_DIR = os.path.dirname(os.path.abspath(__name__))


class TestUtils:
    event_file_path = os.path.join(APP_DIR, "tests", "events", "push_event.json")

    with open(event_file_path, "r") as f:
        payload = json.load(f)

    encoded_payload = json.dumps(payload, separators=(",", ":")).encode()

    def test_verify_signature_with_correct_payload(self, client):

        github_signature = "52d1787b7d4e01d53553b8ef058b86520ea07d28"

        assert verify_signature(github_signature, self.encoded_payload)

    def test_verify_signature_with_wrong_signature(self, client):
        github_signature = "foo"

        assert not verify_signature(github_signature, self.encoded_payload)

    def test_verify_signature_with_wrong_payload(self, client):
        encoded_payload = json.dumps({"foo": "bar"}, separators=(",", ":")).encode()

        github_signature = "52d1787b7d4e01d53553b8ef058b86520ea07d28"

        assert not verify_signature(github_signature, encoded_payload)
