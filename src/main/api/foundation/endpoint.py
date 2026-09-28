from dataclasses import dataclass
from enum import Enum

from src.main.api.models.base_model import BaseModel
from typing import Optional, Type

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.sign_in_user_request import SignInUserRequest
from src.main.api.models.sign_in_user_response import SignInUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse,
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    SIGN_IN_USER = EndpointConfiguration(
        request_model=SignInUserRequest,
        url="/auth/token/login",
        response_model=SignInUserResponse,
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse,
    )
