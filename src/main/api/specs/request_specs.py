import httpx

from src.main.api.configs.config import Config
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.sign_in_user_response import SignInUserResponse


class RequestSpecs:

    @staticmethod
    def base_headers() -> dict:
        return {
            "content-type": "application/json",
            "accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str) -> dict:
        request = SignInUserRequest(username=username, password=password)
        response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers(),
        )
        if response.status_code == 200:
            response_data = SignInUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to login")

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()
