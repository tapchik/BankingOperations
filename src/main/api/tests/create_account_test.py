import pytest
from httpx import Response
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestCreateAccount:

    def test_create_account(self, api_manager: ApiManager, db_session: Session, sign_in_user_request: SignInUserRequest):
        request = sign_in_user_request('ROLE_USER')
        account = api_manager.user_steps.create_an_account(request)
        assert account.balance == 0
        account_from_db = Account.get_account_by_id(db_session, account.id)
        assert account_from_db.id == account.id, 'Аккаунт создан'
        assert account_from_db.balance is not None, 'Поле с балансом есть в БД, не пустое'

    @pytest.mark.parametrize(
        'deposit_amount', [1050.0, 1567.40, 1000.99]
    )
    def test_deposit_to_account_valid(self, api_manager: ApiManager, db_session: Session, deposit_request: (SignInUserRequest, DepositRequest), deposit_amount: float):
        user, deposit = deposit_request('ROLE_USER', deposit_amount)
        deposit_response = api_manager.user_steps.deposit_to_account_valid(user, deposit)
        assert deposit_response.balance == deposit_amount
        account_from_db = Account.get_account_by_id(db_session, deposit.accountId)
        assert account_from_db.id == deposit.accountId, 'Аккаунт создан, есть id'
        assert account_from_db.balance == deposit_amount, 'Баланс аккаунта пополнен в БД'

    @pytest.mark.parametrize(
        'deposit_amount', [500, 9_999, 10_000]
    )
    def test_deposit_to_account_invalid(self, api_manager: ApiManager, db_session: Session, deposit_request: (SignInUserRequest, DepositRequest), deposit_amount: float):
        user, deposit = deposit_request('ROLE_USER', deposit_amount)
        response: Response = api_manager.user_steps.deposit_to_account_invalid(user, deposit)
        assert response.json()['error'] == "Amount must be between 1000 and 9000"
        account_from_db = Account.get_account_by_id(db_session, deposit.accountId)
        assert account_from_db.balance == 0, 'баланс не изменился в БД'

    @pytest.mark.parametrize(
        ['amount_before', 'amount_to_transfer', 'expected'],
        [(2300, 800, 1500), (2000, 2000, 0)]
    )
    def test_transfer_to_account_valid(self, api_manager: ApiManager, db_session: Session, transfer_request: (SignInUserRequest, CreateAccountResponse, CreateAccountResponse, TransferRequest), amount_before: float, amount_to_transfer: float, expected: float):
        sender, senders_deposit, receivers_deposit, request = transfer_request('ROLE_USER', amount_before,
                                                                               'ROLE_USER', amount_before,
                                                                               amount_to_transfer,
                                                                               )
        response = api_manager.user_steps.transfer_to_account_valid(sender, request)
        assert response.fromAccountIdBalance == expected
        sender_from_db = Account.get_account_by_id(db_session, senders_deposit.accountId)
        receiver_from_db = Account.get_account_by_id(db_session, receivers_deposit.accountId)
        assert sender_from_db.balance == amount_before - amount_to_transfer, "Баланс отправителя уменьшился в БД"
        assert receiver_from_db.balance == amount_before + amount_to_transfer, "Баланс получателя пополнился в БД"

    @pytest.mark.parametrize(
        ['amount_before', 'amount_to_transfer'],
        [(2000, 3000), (4000, 4000.01)]
    )
    def test_transfer_to_account_invalid(self, api_manager: ApiManager, db_session: Session, transfer_request: (SignInUserRequest, CreateAccountResponse, CreateAccountResponse, TransferRequest), amount_before: float, amount_to_transfer: float):
        sender, senders_deposit, receivers_deposit, request = transfer_request('ROLE_USER', amount_before,
                                                                               'ROLE_USER', amount_before,
                                                                               amount_to_transfer,
                                                                               )
        response = api_manager.user_steps.transfer_to_account_invalid(sender, request)
        assert response.json()['error'].startswith('Insufficient funds. ')
        sender_from_db = Account.get_account_by_id(db_session, senders_deposit.accountId)
        assert sender_from_db.balance == amount_before, "Баланс отправителя не изменился в БД"
        receiver_from_db = Account.get_account_by_id(db_session, receivers_deposit.accountId)
        assert receiver_from_db.balance == amount_before, "Баланс получателя не изменился в БД"
