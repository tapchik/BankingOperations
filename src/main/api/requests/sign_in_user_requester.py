import httpx

from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.sign_in_user_response import SignInUserResponse
from src.main.api.requests.requester import Requester


class SignInUserRequester(Requester):
    def post(self, sign_in_user_request: SignInUserRequest) -> SignInUserResponse | httpx.Response:
        url = f"{self.base_url}/auth/token/login"
        response = httpx.post(
            url=url,
            json=sign_in_user_request.model_dump()
        )
        self.response_spec(response)
        return SignInUserResponse(**response.json())

