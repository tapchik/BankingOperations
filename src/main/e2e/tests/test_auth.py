from playwright.sync_api import expect

from src.main.e2e.pages.catalog_page import CatalogPage
from src.main.e2e.pages.login_page import LoginPage
from src.main.e2e.steps.catalog_steps import CatalogSteps
from src.main.e2e.steps.login_steps import LoginSteps


class TestAuth:

    def test_auth(self, page):
        steps = LoginSteps(page)
        steps.open_login_page().login("standard_user", "secret_sauce")
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html", timeout=3000)

    def test_invalid_auth(self, page):
        steps = LoginSteps(page)
        steps.open_login_page().login('locked_out_user', 'secret_sauce')
        expect(page).to_have_url(LoginPage.URL)
        assert 'locked out' in steps.get_error_text(), "Ожидаем сообщение о заблокированном пользователе"

    def test_logout(self, page):
        login = LoginSteps(page)
        catalog = CatalogSteps(page)

        login.open_login_page().login("standard_user", "secret_sauce")
        assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

        catalog.logout()
        assert page.url == "https://www.saucedemo.com/", "Ожидаем возврат на страницу логина"

    def test_logout_visual_user(self, page):
        login = LoginSteps(page)
        catalog = CatalogSteps(page)

        login.open_login_page().login("visual_user", "secret_sauce")
        assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

        catalog.logout()
        assert page.url == login.LOGIN_URL, "Ожидаем возврат на страницу логина"
