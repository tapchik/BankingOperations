from playwright.sync_api import expect

from src.main.e2e.pages.login_page import LoginPage


def test_add_item_and_check_in_cart(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login('standard_user', 'secret_sauce')
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    page.locator(".shopping_cart_link").click()

    expect(page.locator("[data-test='secondary-header']:has-text('Your Cart')")).to_be_visible()
    item_name = page.locator('[data-test="inventory-item-name"]')
    assert item_name.inner_text() == "Sauce Labs Backpack"
