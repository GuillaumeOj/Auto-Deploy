class TestRoutes:
    def test_landing_page_with_get(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.data == b"Nothing here..."

    def test_landing_page_with_post(self, client):
        response = client.post(
            "/",
            headers={"X-Hub-Signature": "sha1=37b3c2f2ed573445f2de99a4140b0f23136f65e0"},
            data={"foo": "bar"},
        )
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Everything is ok!"

    def test_landing_page_with_no_signature(self, client):
        response = client.post("/", data={"foo": "bar"})
        assert response.status_code == 403
        assert response.data.decode("utf-8") == "The signature is missing"

    def test_landing_page_with_wrong_signature(self, client):
        response = client.post(
            "/", headers={"X-Hub-Signature": "sha1=foo"}, data={"foo": "bar"}
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
