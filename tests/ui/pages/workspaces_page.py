import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ui.pages.base_page import BasePage


class WorkspacesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Form locators
        self.form_name_locator = (By.ID, "name")
        self.form_slug_locator = (By.ID, "slug")
        self.form_timezone_locator = (By.ID, "timezone")
        self.form_create_btn_locator = (By.CSS_SELECTOR, "button[type='submit']")
        self.form_error_locator = (By.CSS_SELECTOR, ".form-error")

        # Dashboard & Sidebar locators
        self.sidebar_locator = (
            By.CSS_SELECTOR,
            "[data-sidebar='sidebar'], [data-slot='sidebar']",
        )
        self.workspace_select_trigger_locator = (
            By.CSS_SELECTOR,
            "button[role='combobox'], [data-sidebar='header'] button, [data-slot='sidebar-header'] button",
        )
        self.create_workspace_link_locator = (
            By.XPATH,
            "//a[contains(@href, '/workspace/create')]",
        )

    @allure.step("Navigate to create workspace page")
    def navigate_to_create(self):
        self.navigate("workspace/create")

    @allure.step("Navigate to workspace dashboard for slug '{slug}'")
    def navigate_to_workspace(self, slug: str):
        self.navigate(f"workspace/{slug}")
        self.wait_for_sidebar_loaded(slug)

    @allure.step("Wait for workspace sidebar ORPC data to load for slug '{slug}'")
    def wait_for_sidebar_loaded(self, slug: str, timeout=15):
        locator = (
            By.XPATH,
            f"//a[contains(@href, '/workspace/{slug}/settings/')]",
        )
        return self.is_element_present(locator, timeout=timeout)

    @allure.step("Verify create workspace form is rendered")
    def is_create_workspace_form_rendered(self):
        return (
            self.is_element_present(self.form_name_locator)
            and self.is_element_present(self.form_slug_locator)
            and self.is_element_present(self.form_timezone_locator)
            and self.is_element_present(self.form_create_btn_locator)
        )

    @allure.step(
        "Create workspace with name '{name}', slug '{slug}', timezone '{timezone}'"
    )
    def create_workspace(
        self, name: str, slug: str, timezone: str = "UTC", wait_for_redirect=True
    ):
        name_field = self.find(self.form_name_locator)
        name_field.clear()
        name_field.send_keys(name)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            name_field,
        )

        slug_field = self.find(self.form_slug_locator)
        slug_field.clear()
        slug_field.send_keys(slug)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            slug_field,
        )

        tz_field = self.find(self.form_timezone_locator)
        tz_field.clear()
        tz_field.send_keys(timezone)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            tz_field,
        )

        self.click(self.form_create_btn_locator)

        if wait_for_redirect:
            WebDriverWait(self.driver, 15).until(
                EC.url_contains(f"/workspace/{slug}"),
                message=f"Timed out waiting for URL redirect to '/workspace/{slug}' after creation. Current URL is '{self.driver.current_url}'",
            )

    @allure.step("Get form validation error message")
    def get_form_error_text(self):
        if self.is_element_present(self.form_error_locator, timeout=5):
            return self.get_text(self.form_error_locator)
        return ""

    @allure.step("Verify workspace dashboard layout is rendered")
    def is_dashboard_layout_rendered(self):
        return self.is_element_present(self.sidebar_locator)

    @allure.step("Open workspace selector dropdown")
    def open_workspace_selector(self):
        self.click(self.workspace_select_trigger_locator)

    @allure.step("Select workspace '{slug_or_name}' from selector dropdown")
    def select_workspace_from_dropdown(self, slug_or_name: str):
        item_locator = (
            By.XPATH,
            f"//div[@role='listbox']//div[@role='option'][contains(., '{slug_or_name}')] | //*[@role='option'][contains(., '{slug_or_name}')]",
        )
        self.click(item_locator)

    @allure.step("Navigate to workspace settings sub-route '{setting_name}'")
    def click_settings_link(self, setting_name: str, slug: str = ""):
        if slug:
            link_locator = (
                By.XPATH,
                f"//a[contains(@href, '/workspace/{slug}/settings/') and (contains(., '{setting_name}') or .//span[contains(text(), '{setting_name}')])]",
            )
        else:
            link_locator = (
                By.XPATH,
                f"//a[contains(@href, '/settings/') and not(contains(@href, '/workspace//settings/')) and (contains(., '{setting_name}') or .//span[contains(text(), '{setting_name}')])]",
            )
        self.click(link_locator)
