from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad(),
        ).post(create_user_request)

    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            endpoint=Endpoint.ADMIN_DELETE_USER,
            response_spec=ResponseSpecs.request_ok(),
        ).delete(user_id)

    def sign_in_user(self, sign_in_user_request: SignInUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.SIGN_IN_USER,
            ResponseSpecs.request_ok(),
        ).post(sign_in_user_request)
        return response
