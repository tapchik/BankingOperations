import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:

    @pytest.mark.parametrize(
        'create_user_request',
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_valid(self, api_manager: ApiManager, db_session: Session, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.create_user(create_user_request)
        assert response.username == create_user_request.username
        assert response.role == create_user_request.role
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Пользователь появился в БД'

    @pytest.mark.parametrize(
        ["username", "password", "message"],
        [
            ("ПавеL", "Lento4ka5%", "логин: латиница + кириллица"),
            ("Xi", "Lento4ka5%", "логин: <3 символов"),
            ("veronikastepanovna", "Lento4ka5%", "логин: >15 символов"),
            ("dianka$uchka", "Lento4ka5%", "логин: спецсимволы"),
            ("Leon", "L$a5", "пароль: <8 символов"),
            ("Leon", "watermar5", "пароль: нет заглавных"),
        ]
    )
    def test_create_user_invalid(self, api_manager: ApiManager, db_session: Session, username: str, password: str, message: str):
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, 'Пользователь не создан, т.к. не прошёл валидацию'

