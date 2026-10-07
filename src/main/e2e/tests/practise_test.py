import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.mark.e2e
class TestPractice:

    def test_text_box(self, page):
        page.goto("https://demoqa.com/text-box")
        page.locator("input#userName").fill('LANA')
        email_field = page.locator("#userEmail")
        email_field.fill('rama')
        page.locator('#currentAddress').fill("Ленина")
        page.locator('#permanentAddress').fill("Герасимова")
        page.click('#submit')

    def test_checkboxes(self, page):
        page.goto("https://demoqa.com/checkbox")

        expect(page.locator("div#result")).not_to_be_attached()
        page.get_by_role('checkbox').first.click()
        expect(page.locator("div#result")).to_be_attached()

    def test_radio_buttons(self, page):
        page.goto("https://demoqa.com/radio-button")
        result_box = page.locator("p.mt-3")
        # result_field = page.locator("span.text-success")
        expect(page.get_by_role('radio', name='no')).to_be_disabled()
        expect(result_box).not_to_be_attached()
        page.get_by_role('radio', name='yes').check()
        expect(result_box).to_be_visible()
        expect(result_box).to_contain_text("You have selected Yes")
        page.get_by_role('radio', name='impressive').check()
        expect(result_box).to_contain_text("You have selected Impressive")

    def test_clicks_and_links(self, page):
        page.goto("https://demoqa.com/buttons")

        single_click_btn = page.locator("button:text-is('Click Me')")
        dbl_click_btn = page.locator("button:text-is('Double Click Me')")
        right_click_btn = page.locator("button:text-is('Right Click Me')")

        result = page.locator("div.mt-4")
        single_click_message = result.filter(has_text="You have done a dynamic click")
        dbl_click_message = result.filter(has_text="You have done a double click")
        right_click_message = result.filter(has_text="You have done a right click")

        expect(single_click_message).not_to_be_visible()
        expect(dbl_click_message).not_to_be_visible()
        expect(right_click_message).not_to_be_visible()

        single_click_btn.click()
        dbl_click_btn.dblclick()
        right_click_btn.click(button='right')

        expect(single_click_message).to_be_visible()
        expect(dbl_click_message).to_be_visible()
        expect(right_click_message).to_be_visible()

    def test_upload_download(self, page, tmp_path):

        page.goto("https://demoqa.com/upload-download")

        # Создаём временный файл для загрузки
        file_path = tmp_path / "demoqa_test_file.txt"
        file_path.write_text("Hello, this is a test file for DemoQA upload!")

        # Загружаем файл
        page.set_input_files("#uploadFile", str(file_path))

        # Проверяем, что имя файла отобразилось на странице
        uploaded_file_name = page.locator("#uploadedFilePath")
        assert file_path.name in uploaded_file_name.inner_text()

    @pytest.mark.skip
    def test_date_picker_select_option(self, page):
        page.goto("https://demoqa.com/date-picker")

        # Локатор поля даты
        date_input = page.locator("#dateAndTimePickerInput")
        date_input.click()  # открываем календарь

        # Выбираем месяц и год через select_option
        page.locator(".react-datepicker__month-select").select_option("7")  # август (0-based)
        page.locator(".react-datepicker__year-select").select_option("2025")  # год

        # Выбираем день (например, 25-е число)
        page.locator(".react-datepicker__day--025").click()

        # Проверяем, что значение инпута изменилось
        assert date_input.input_value() == "08/25/2025"
