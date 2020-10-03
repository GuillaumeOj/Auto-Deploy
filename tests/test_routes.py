class TestRoutes:
    def test_landing_page_with_get(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.data == b"Nothing here..."

    def test_landing_page_with_post(self, client):
        response = client.post("/", data={"foo": "bar"})
        assert response.status_code == 200
