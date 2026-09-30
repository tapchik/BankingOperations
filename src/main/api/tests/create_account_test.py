import pytest
from httpx import Response
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestCreateAccount:

    def test_create_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Аккаунт создан'
        assert account_from_db.balance is not None, 'Поле с балансом есть в БД, не пустое'

    def test_deposit_to_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_user_request)
        assert create_account_response.balance == 0
        new_account_id = create_account_response.id
        sign_in_request = SignInUserRequest(username=create_user_request.username, password=create_user_request.password)
        deposit_request = DepositRequest(account_id=new_account_id, amount=1050.0)
        deposit_response = api_manager.user_steps.deposit_to_account_valid(sign_in_request, deposit_request)
        assert deposit_response.balance == 1050

    def test_deposit_to_account_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        create_account_response = api_manager.user_steps.create_account(create_user_request)
        assert create_account_response.balance == 0
        new_account_id = create_account_response.id
        sign_in_request = SignInUserRequest(username=create_user_request.username,
                                            password=create_user_request.password)
        deposit_request = DepositRequest(account_id=new_account_id, amount=50.0)
        response: Response = api_manager.user_steps.deposit_to_account_invalid(sign_in_request, deposit_request)
        assert response.status_code == 400
        assert response.json()['error'] == "Amount must be between 1000 and 9000"

    @pytest.mark.parametrize(
        ['amount_before', 'amount_to_transfer', 'expected'],
        [(2300, 800, 1500), (2000, 2000, 0)]
    )
    def test_transfer_to_account_valid(self, api_manager: ApiManager, create_account_with_balance, amount_before, amount_to_transfer, expected):
        sender = create_account_with_balance(amount_before)
        receiver = create_account_with_balance(amount_before)
        transfer_request = TransferRequest(
            from_account_id=sender.account.id,
            to_account_id=receiver.account.id,
            amount=amount_to_transfer)
        response = api_manager.user_steps.transfer_to_account_valid(sender.user, transfer_request)
        assert response.fromAccountIdBalance == expected

