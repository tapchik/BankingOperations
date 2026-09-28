import pytest
import httpx


@pytest.mark.api
class TestAdminActions:

    def test_create_user(self):
        r = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            }
        )
        token = r.json().get("token")

        r = httpx.get(
            url="http://localhost:4111/api/admin/users",
            headers={
                "content-type": "application/json",
                "Authorization": "Bearer " + token
            }
        )

        one = r.json()[0]
        assert one['id'] == 1
        assert one['username'] == 'admin'
        assert one['role'] == 'ROLE_ADMIN'

