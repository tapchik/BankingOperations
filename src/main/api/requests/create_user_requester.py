from http import HTTPStatus
import httpx

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.requester import Requester


class CreateUserRequester(Requester):
    def post(self, create_user_request: CreateUserRequest) -> CreateUserResponse | httpx.Response:
        url = f"{self.base_url}/admin/create"
        response = httpx.post(
            url=url,
            json=create_user_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return CreateUserResponse(**response.json())
        return response
