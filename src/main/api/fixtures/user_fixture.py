from typing import Callable, Any, Literal

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.structures_for_tests.structures import UserWithAccount


UserRole = Literal["ROLE_USER", "ROLE_CREDIT_SECRET"]


@pytest.fixture
def create_user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_new_user(api_manager: ApiManager) -> Callable[[UserRole], CreateUserRequest]:
    """Admin creates a new user with generated username and password and specified role"""
    def _create(user_role: UserRole) -> CreateUserRequest:
        user_request = RandomModelGenerator.generate(CreateUserRequest)
        user_request.role = user_role
        api_manager.admin_steps.create_user(user_request)
        return user_request
    yield _create


@pytest.fixture
def create_account_with_balance(api_manager: ApiManager) -> Callable[[CreateUserRequest, int], UserWithAccount]:
    """Creates a user, and account for him and deposits a specified amount to it. Returns id: int of a created account"""
    def _create(create_user_request, amount=0):
        create_account_response = api_manager.user_steps.create_account(create_user_request)
        new_account_id = create_account_response.id
        sign_in_request = SignInUserRequest(username=create_user_request.username,
                                            password=create_user_request.password)
        if amount:
            deposit_request = DepositRequest(account_id=new_account_id, amount=amount)
            api_manager.user_steps.deposit_to_account_valid(sign_in_request, deposit_request)
            create_account_response.balance = amount
        user_with_account = UserWithAccount(
            user=SignInUserRequest(username=create_user_request.username, password=create_user_request.password),
            account=create_account_response,
        )
        return user_with_account
    return _create
