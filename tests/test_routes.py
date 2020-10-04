import json
import os
import subprocess

import pytest

from webhooks import hooks


APP_DIR = os.path.dirname(os.path.abspath(__name__))


def mock_subprocess_run(*args, **kwargs):
    return subprocess.CompletedProcess


class TestRoutes:
    data_path = os.path.join(APP_DIR, "tests", "events", "push_event.json")

    with open(data_path, "r") as f:
        payload = json.load(f)

    data = json.dumps(payload, separators=(",", ":"))

    def test_landing_page_with_get(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.data == b"Nothing here..."

    def test_landing_page_with_post(self, client, monkeypatch):
        monkeypatch.setattr("subprocess.run", mock_subprocess_run)

        custom_payload = self.payload
        custom_payload["ref"] = "refs/heads/master"

        custom_data = json.dumps(custom_payload, separators=(",", ":"))

        response = client.post(
            "/",
            headers={
                "X-GitHub-Event": "push",
                "X-Hub-Signature": "sha1=8269e9712c991666e0a4f02f6c7fd95f08ef2eb1",
            },
            data=custom_data,
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Thanks!"

    def test_landing_page_with_no_signature(self, client):
        response = client.post("/", data={"foo": "bar"})
        assert response.status_code == 403
        assert response.data.decode("utf-8") == "The signature is missing"

    def test_landing_page_with_wrong_signature(self, client, monkeypatch):
        response = client.post(
            "/",
            headers={
                "X-GitHub-Event": "push",
                "X-Hub-Signature": "sha1=foo",
            },
            data=self.data,
            content_type="application/json",
        )
        assert response.status_code == 403
        assert (
            response.data.decode("utf-8")
            == "The given signature don't match with the payload"
        )

    def test_landing_page_with_wrong_syntax_in_signature(self, client):
        response = client.post(
            "/", headers={"X-Hub-Signature": "sha1foo"}, data={"foo": "bar"}
        )
        assert response.status_code == 403
        assert (
            response.data.decode("utf-8")
            == "The given signature don't match the expected form"
        )

    def test_landing_page_with_wrong_digest_mode(self, client):
        response = client.post(
            "/", headers={"X-Hub-Signature": "sha512=foo"}, data={"foo": "bar"}
        )
        assert response.status_code == 403
        assert response.data.decode("utf-8") == "Only sha1 could be used"

    def test_landing_page_with_wrong_branch(self, client):
        response = client.post(
            "/",
            headers={
                "X-GitHub-Event": "push",
                "X-Hub-Signature": "sha1=3c08584faa506a2add1d18ca7fe182e80924dc79",
            },
            data=self.data,
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Thanks!"

    def test_landing_page_with_undeclared_repository(self, client):
        custom_payload = self.payload
        custom_payload["repository"]["name"] = "foo"

        custom_data = json.dumps(custom_payload, separators=(",", ":"))

        response = client.post(
            "/",
            headers={
                "X-GitHub-Event": "push",
                "X-Hub-Signature": "sha1=e141bd8ed6106fed6ec06965d26f6c391ac379ae",
            },
            data=custom_data,
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Thanks!"

    def test_landing_page_with_wrong_event(self, client):
        response = client.post(
            "/",
            headers={
                "X-GitHub-Event": "pull_request",
                "X-Hub-Signature": "sha1=3c08584faa506a2add1d18ca7fe182e80924dc79",
            },
            data=self.data,
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Thanks!"
