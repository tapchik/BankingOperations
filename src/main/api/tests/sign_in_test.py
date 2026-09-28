from src.main.api.models.sign_in_user_request import SignInUserRequest


#  @pytest.mark.api
class TestSignIn:

    def test_sign_in_as_admin(self, api_manager):
        sign_in_admin_request = SignInUserRequest(username='admin', password='123456')
        response = api_manager.admin_steps.sign_in_user(sign_in_admin_request)
        assert response.user.username == sign_in_admin_request.username
        assert response.user.role == 'ROLE_ADMIN'

    def test_sign_in_as_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.sign_in_user(create_user_request)
        assert response.user.username == create_user_request.username
        assert response.user.role == 'ROLE_USER'
