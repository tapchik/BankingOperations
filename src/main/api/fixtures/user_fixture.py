from typing import Callable, Any, Literal, Tuple

import pytest
from sqlalchemy import Float

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit.credit_request_request import CreditRequestRequest
from src.main.api.models.credit.credit_request_response import CreditRequestResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.transfer_request import TransferRequest

#  from src.main.api.structures_for_tests.structures import UserWithAccount


UserRole = Literal["ROLE_USER", "ROLE_CREDIT_SECRET"]


@pytest.fixture
def sign_in_user_request(api_manager: ApiManager) -> Callable[[UserRole], SignInUserRequest]:
    def _create(user_rule: UserRole) -> SignInUserRequest:
        create_user_request = RandomModelGenerator.generate(CreateUserRequest)
        if user_rule == 'ROLE_CREDIT_SECRET':
            create_user_request.role = 'ROLE_CREDIT_SECRET'
        api_manager.admin_steps.create_user(create_user_request)
        sign_in_user_request = SignInUserRequest(username=create_user_request.username,
                                                 password=create_user_request.password)
        return sign_in_user_request
    return _create


@pytest.fixture
def an_account(api_manager: ApiManager, sign_in_user_request: SignInUserRequest) -> Callable[[UserRole], tuple[SignInUserRequest, CreateAccountResponse]]:
    def _create(user_rule: UserRole) -> (SignInUserRequest, CreateAccountResponse):
        sign_in = sign_in_user_request(user_rule)
        create_account_response = api_manager.user_steps.create_an_account(sign_in)
        return sign_in, create_account_response
    return _create


@pytest.fixture
def deposit_request(api_manager: ApiManager, an_account: SignInUserRequest) -> Callable[[UserRole, float], tuple[SignInUserRequest, CreateAccountResponse, DepositRequest]]:
    """Works nicely"""
    def _create(user_role: UserRole, deposit_amount: float) -> (SignInUserRequest, CreateAccountResponse, DepositRequest):
        sign_in, account = an_account(user_role)
        deposit_request = DepositRequest(account_id=account.id, amount=deposit_amount)
        return sign_in, account, deposit_request
    return _create


@pytest.fixture
def an_account_with_balance(api_manager: ApiManager, deposit_request: (SignInUserRequest, CreateAccountResponse)) -> Callable[[UserRole, float], tuple[SignInUserRequest, CreateAccountResponse]]:
    def _create(user_rule: UserRole, balance: float) -> (SignInUserRequest, DepositRequest):
        user, account, deposit = deposit_request(user_rule, balance)
        api_manager.user_steps.deposit_to_account_valid(user, deposit)
        return user, account
    return _create


@pytest.fixture
def transfer_request(api_manager: ApiManager, an_account_with_balance: (SignInUserRequest, CreateAccountResponse)) -> Callable[[UserRole, float, UserRole, float, float], tuple[SignInUserRequest, CreateAccountResponse, CreateAccountResponse, TransferRequest]]:
    def _create(sender_role: UserRole, senders_account_balance: float, receiver_role: UserRole, receivers_account_balance: float, amount_to_transfer: float) -> (SignInUserRequest, CreateAccountResponse, CreateAccountResponse, TransferRequest):
        sender, senders_account = an_account_with_balance(sender_role, senders_account_balance)
        receiver, receivers_account = an_account_with_balance(receiver_role, receivers_account_balance)
        transfer_request = TransferRequest(from_account_id=senders_account.id,
                                           to_account_id=receivers_account.id,
                                           amount=amount_to_transfer)
        return sender, senders_account, receivers_account, transfer_request
    return _create


@pytest.fixture
def credit_request_request(api_manager: ApiManager, an_account_with_balance: (SignInUserRequest, CreateAccountResponse)) -> Callable[[UserRole, float, float, int], tuple[SignInUserRequest, CreditRequestRequest]]:
    def _create(user_role: UserRole, account_balance: float, credit_amount: float, months: int) -> (SignInUserRequest, CreditRequestRequest):
        user, account = an_account_with_balance(user_role, account_balance)
        request = CreditRequestRequest(account_id=account.id,
                                       amount=credit_amount,
                                       term_months=months)
        return user, request
    return _create


@pytest.fixture
def credit_repay(api_manager: ApiManager, credit_request_request) -> Callable[[float, float, int, float], tuple[SignInUserRequest, CreditRepayRequest]]:
    def _create(account_balance: float, credit_amount: float, months: int, repay_amount: float) -> (SignInUserRequest, CreditRepayRequest):
        sign_in, credit_request = credit_request_request('ROLE_CREDIT_SECRET', account_balance, credit_amount, months)
        credit_response = api_manager.user_steps.request_credit_valid(sign_in, credit_request)
        repay_request = CreditRepayRequest(credit_id=credit_response.creditId,
                                           account_id=credit_response.id,
                                           amount=repay_amount)
        return sign_in, repay_request
    return _create