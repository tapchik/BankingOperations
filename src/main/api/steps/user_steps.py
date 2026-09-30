from httpx import Response

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):

    def create_account(self, create_user_request: CreateUserRequest) -> CreateAccountResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post()
        return response

    def deposit_to_account_valid(self, sign_in_user_request: SignInUserRequest, deposit_request: DepositRequest) -> DepositResponse:
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=sign_in_user_request.username, password=sign_in_user_request.password),
            Endpoint.DEPOSIT_TO_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(deposit_request)
        return response

    def deposit_to_account_invalid(self, sign_in_user_request: SignInUserRequest, deposit_request: DepositRequest) -> Response:
        response = CrudRequester(
            RequestSpecs.auth_headers(username=sign_in_user_request.username, password=sign_in_user_request.password),
            Endpoint.DEPOSIT_TO_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(deposit_request)
        return response
