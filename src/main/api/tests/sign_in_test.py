from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.sign_in_user_request import SignInUserRequest


#  @pytest.mark.api
class TestSignIn:

    def test_sign_in_as_admin(self, api_manager: ApiManager):
        sign_in_admin_request = SignInUserRequest(username='admin', password='123456')
        response = api_manager.admin_steps.sign_in_user(sign_in_admin_request)
        assert response.user.username == sign_in_admin_request.username
        assert response.user.role == 'ROLE_ADMIN'

    def test_sign_in_as_user(self, api_manager: ApiManager, sign_in_user_request: SignInUserRequest):
        request = sign_in_user_request('ROLE_USER')
        response = api_manager.admin_steps.sign_in_user(request)
        assert response.user.username == request.username
        assert response.user.role == 'ROLE_USER'
