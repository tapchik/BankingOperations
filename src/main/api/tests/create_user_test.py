import pytest
import httpx

from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.sign_in_user_response import SignInUserResponse
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:

    def test_create_user_valid(self):
        create_user_request = CreateUserRequest(username='PtichKaa', password='LevoV0$5', role='ROLE_USER')
        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)
        assert response.username == create_user_request.username
        assert response.role == create_user_request.role


    @pytest.mark.parametrize(["username", "password", "message"], [
        ("ПавеL", "Lento4ka5%", "логин: латиница + кириллица"),
        ("Xi", "Lento4ka5%", "логин: <3 символов"),
        ("veronikastepanovna", "Lento4ka5%", "логин: >15 символов"),
        ("dianka$uchka", "Lento4ka5%", "логин: спецсимволы"),
        ("Leon", "L$a5", "пароль: <8 символов"),
        ("Leon", "watermar5", "пароль: нет заглавных"),
    ])
    def test_create_user_invalid(self, username, password, message):

        sign_in_admin_request = SignInUserRequest(username='admin', password='123456')
        response = httpx.post(
            url="http://localhost:4111/api/auth/token/login",
            json=sign_in_admin_request.model_dump()
        )
        token = response.json().get("token")

        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        response = httpx.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "content-type": "application/json",
                "Authorization": "Bearer " + token
            }
        )

        assert response.status_code == 400
        ## create_user_response = CreateUserResponse(**response.json())