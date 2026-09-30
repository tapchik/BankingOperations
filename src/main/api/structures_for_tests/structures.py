from dataclasses import dataclass

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.sign_in_user_request import SignInUserRequest


@dataclass
class UserWithAccount:
    user: SignInUserRequest
    account: CreateAccountResponse
