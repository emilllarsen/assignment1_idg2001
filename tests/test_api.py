"""API endpoint integration tests."""


class TestUsers:
    def test_create_user(self, client):
        resp = client.post("/v1/user", json={
            "email": "test@example.com",
            "password": "secret123",
        })
        assert resp.status_code == 201
        assert resp.json()["email"] == "test@example.com"
        assert resp.json()["tokens"] == 10

    def test_duplicate_user(self, client):
        client.post("/v1/user", json={
            "email": "dupe@test.com", "password": "secret123",
        })
        resp = client.post("/v1/user", json={
            "email": "dupe@test.com", "password": "other456",
        })
        assert resp.status_code == 409

    def test_get_user(self, client):
        create = client.post("/v1/user", json={
            "email": "find@test.com", "password": "secret123",
        })
        user_id = create.json()["id"]
        resp = client.get(f"/v1/user/{user_id}")
        assert resp.status_code == 200
        assert resp.json()["email"] == "find@test.com"

    def test_delete_user(self, client):
        create = client.post("/v1/user", json={
            "email": "delete@test.com", "password": "secret123",
        })
        user_id = create.json()["id"]
        resp = client.delete(f"/v1/user/{user_id}")
        assert resp.status_code == 204


class TestTokens:
    def test_add_tokens(self, client):
        create = client.post("/v1/user", json={
            "email": "token@test.com", "password": "secret123",
        })
        user_id = create.json()["id"]
        resp = client.post("/v1/tokens", json={
            "user_id": user_id, "amount": 5,
        })
        assert resp.json()["tokens"] == 15

    def test_token_consumption(self, client):
        create = client.post("/v1/user", json={
            "email": "consume@test.com", "password": "secret123",
        })
        user_id = create.json()["id"]

        # Call a data endpoint
        client.get("/v1/country/USA", headers={"X-User-Id": user_id})

        # Check tokens went down
        resp = client.get(f"/v1/user/{user_id}")
        assert resp.json()["tokens"] == 9

    def test_no_tokens_returns_403(self, client):
        create = client.post("/v1/user", json={
            "email": "broke@test.com", "password": "secret123",
        })
        user_id = create.json()["id"]

        # Use all 10 tokens
        for _ in range(10):
            client.get("/v1/country/USA", headers={"X-User-Id": user_id})

        # 11th call should fail
        resp = client.get("/v1/country/USA", headers={"X-User-Id": user_id})
        assert resp.status_code == 403
