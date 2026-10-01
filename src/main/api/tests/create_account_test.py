import pytest
from httpx import Response
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit.credit_request_request import CreditRequestRequest
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

    @pytest.mark.parametrize(
        'deposit_amount', [1050.0, 1567.40, 1000.99]
    )
    def test_deposit_to_account_valid(self, api_manager, create_new_user, deposit_amount):
        user = create_new_user('ROLE_USER')
        account = api_manager.user_steps.create_account(user)
        sign_in_request = SignInUserRequest(username=user.username, password=user.password)
        deposit_request = DepositRequest(account_id=account.id, amount=deposit_amount)
        deposit_response = api_manager.user_steps.deposit_to_account_valid(sign_in_request, deposit_request)
        assert deposit_response.balance == deposit_amount

    @pytest.mark.parametrize(
        'deposit_amount', [500, 9_999, 10_000]
    )
    def test_deposit_to_account_invalid(self, api_manager, create_new_user, deposit_amount):
        user = create_new_user('ROLE_USER')
        account = api_manager.user_steps.create_account(user)
        sign_in_request = SignInUserRequest(username=user.username,
                                            password=user.password)
        deposit_request = DepositRequest(account_id=account.id, amount=deposit_amount)
        response: Response = api_manager.user_steps.deposit_to_account_invalid(sign_in_request, deposit_request)
        assert response.status_code == 400
        assert response.json()['error'] == "Amount must be between 1000 and 9000"

    @pytest.mark.parametrize(
        ['amount_before', 'amount_to_transfer', 'expected'],
        [(2300, 800, 1500), (2000, 2000, 0)]
    )
    def test_transfer_to_account_valid(self, api_manager, create_new_user, create_account_with_balance, amount_before, amount_to_transfer, expected):
        sender = create_account_with_balance(create_new_user('ROLE_USER'), amount_before)
        receiver = create_account_with_balance(create_new_user('ROLE_USER'), amount_before)
        transfer_request = TransferRequest(
            from_account_id=sender.account.id,
            to_account_id=receiver.account.id,
            amount=amount_to_transfer)
        response = api_manager.user_steps.transfer_to_account_valid(sender.user, transfer_request)
        assert response.fromAccountIdBalance == expected

    @pytest.mark.parametrize(
        ['amount_before', 'amount_to_transfer'],
        [(2000, 3000), (4000, 4000.01)]
    )
    def test_transfer_to_account_invalid(self, api_manager, create_new_user, create_account_with_balance, amount_before, amount_to_transfer):
        sender = create_account_with_balance(create_new_user('ROLE_USER'), amount_before)
        receiver = create_account_with_balance(create_new_user('ROLE_USER'), amount_before)
        transfer_request = TransferRequest(
            from_account_id=sender.account.id,
            to_account_id=receiver.account.id,
            amount=amount_to_transfer)
        response = api_manager.user_steps.transfer_to_account_invalid(sender.user, transfer_request)
        assert response.status_code == 422
        assert response.json()['error'].startswith('Insufficient funds. ')

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'term_months'],
        [(9000, 10_000, 12), (3000, 5000, 9)]
    )
    def test_request_credit_valid(self, api_manager, create_new_user, create_account_with_balance, account_balance, credit_amount, term_months):
        user = create_new_user('ROLE_CREDIT_SECRET')
        context = create_account_with_balance(user, account_balance)
        credit_request_request = CreditRequestRequest(account_id=context.account.id, amount=credit_amount, term_months=term_months)
        response = api_manager.user_steps.request_credit_valid(context.user, credit_request_request)
        assert response.amount == credit_amount
        assert response.balance == account_balance + credit_amount

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'term_months'], [(9000, 10_000, 12)]
    )
    def test_request_credit_invalid(self, api_manager, create_new_user, create_account_with_balance, account_balance, credit_amount, term_months):
        user = create_new_user('ROLE_USER')
        context = create_account_with_balance(user, account_balance)
        credit_request_request = CreditRequestRequest(account_id=context.account.id, amount=credit_amount,
                                                      term_months=term_months)
        response = api_manager.user_steps.request_credit_invalid(context.user, credit_request_request)
        assert response.status_code == 403
        assert response.json()['detail'] == 'Forbidden: ROLE_CREDIT access required'

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'repay_amount'],
        [(5000, 10_000, 10_000), (9000, 15_000, 15_000)]
    )
    def test_repay_credit_valid(self, api_manager, create_account, account_balance, credit_amount, repay_amount):
        user, credit = create_account(account_balance, credit_amount)
        credit_repay_request = CreditRepayRequest(credit_id=credit.creditId, account_id=credit.id, amount=repay_amount)
        response = api_manager.user_steps.repay_credit_valid(user, credit_repay_request)
        assert response.creditId == credit.creditId
        assert response.amountDeposited == repay_amount
