import pytest
from httpx import Response
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestRequestCredit:

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'term_months'],
        [(9000, 10_000, 12), (3000, 5000, 9)]
    )
    def test_request_credit_valid(self, api_manager: ApiManager, db_session: Session, credit_request_request: (SignInUserRequest, CreditRequestRequest), account_balance: float, credit_amount: float, term_months: int):
        user, request = credit_request_request('ROLE_CREDIT_SECRET', account_balance, credit_amount, term_months)
        credit_response = api_manager.user_steps.request_credit_valid(user, request)
        assert credit_response.amount == credit_amount
        assert credit_response.balance == account_balance + credit_amount
        credit_from_db = Credit.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.amount == credit_amount, "Сумма выданного кредита правильная в БД"
        assert credit_from_db.balance == -credit_amount, "Баланс выданного кредита правильный в БД"

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'term_months'], [(9000, 10_000, 12)]
    )
    def test_request_credit_invalid(self, api_manager: ApiManager, db_session: Session, credit_request_request: (SignInUserRequest, CreditRequestRequest), account_balance: float, credit_amount: float, term_months: int):
        user, request = credit_request_request('ROLE_USER', account_balance, credit_amount, term_months)
        response = api_manager.user_steps.request_credit_invalid(user, request)
        assert response.json()['detail'] == 'Forbidden: ROLE_CREDIT access required'
        credit_from_db = Credit.get_credit_by_account_id(db_session, request.accountId)
        assert credit_from_db is None, "Кредит не выдан, нет записи в БД"

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'repay_amount'],
        [(5000.0, 10_000.0, 10_000.0), (9000.0, 15_000.0, 15_000.0)]
    )
    def test_repay_credit_valid(self, api_manager: ApiManager, db_session: Session, credit_repay: (SignInUserRequest, CreditRepayRequest), account_balance: float, credit_amount: float, repay_amount: float):
        sign_in, repay_request = credit_repay(account_balance, credit_amount, 12, repay_amount)
        repay_response = api_manager.user_steps.repay_credit_valid(sign_in, repay_request)
        assert repay_response.creditId == repay_request.creditId
        assert repay_response.amountDeposited == repay_amount
        credit_from_db = Credit.get_credit_by_id(db_session, repay_response.creditId)
        assert credit_from_db.balance == 0, "Кредит полностью погашен в БД"

    @pytest.mark.parametrize(
        ['account_balance', 'credit_amount', 'repay_amount'],
        [(5000.0, 10_000.0, 9_000.0), (9000.0, 15_000.0, 5_000.0)]
    )
    def test_repay_credit_invalid(self, api_manager: ApiManager, db_session: Session, credit_repay: (SignInUserRequest, CreditRepayRequest), account_balance: float, credit_amount: float, repay_amount: float):
        sign_in, repay_request = credit_repay(account_balance, credit_amount, 12, repay_amount)
        response = api_manager.user_steps.repay_credit_invalid(sign_in, repay_request)
        assert response.json()['error'].startswith('The amount is not enough')
        credit_from_db = Credit.get_credit_by_account_id(db_session, repay_request.creditId)
        assert credit_from_db is None, "Кредит не выдан, нет записи в БД"
