import allure
from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage


class TeamsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Sidebar Locators
        self.your_teams_locator = (
            By.XPATH,
            "//a[.//span[normalize-space()='Your teams']] | //span[normalize-space()='Your teams']",
        )
        self.issues_locator = (
            By.XPATH,
            "//a[.//span[normalize-space()='Issues']]",
        )
        self.cycles_locator = (
            By.XPATH,
            "//a[.//span[normalize-space()='Cycles']]",
        )

        self.settings_locator = (By.CSS_SELECTOR, "//*[name()='circle']")

        self.default_team_locator = (
            By.XPATH,
            "//span[normalize-space()='Default Team']",
        )
        self.manage_teams_locator = (By.CSS_SELECTOR, 'a[href="/workspace/t/teams"]')

        self.teams_table_locator = (By.CSS_SELECTOR, 'table[data-slot="table"]')
        # Issues page locators

        # Cycles page locators
        self.create_cycle_btn_locator = (
            By.XPATH,
            "//button[.//span[normalize-space()='Create cycle']]",
        )

    @allure.step("Check if 'Your teams' section is present")
    def is_your_teams_section_present(self) -> bool:
        return self.is_element_present(self.your_teams_locator)

    @allure.step("Click 'Your teams' header link")
    def click_your_teams(self):
        self.click(self.your_teams_locator)

    @allure.step("Default Team  Element Visibility")
    def is_default_team_present(self) -> bool:
        return self.is_element_present(self.default_team_locator)

    @allure.step("Click Default Team Toggle")
    def click_default_team(self):
        self.click(self.default_team_locator)

    @allure.step("Check if 'Issues' link is present")
    def is_issues_link_present(self) -> bool:
        return self.is_element_present(self.issues_locator)

    @allure.step("Check if 'Cycles' link is present")
    def is_cycles_link_present(self) -> bool:
        return self.is_element_present(self.cycles_locator)

    @allure.step("Click 'Issues' link in sidebar")
    def click_issues(self):
        self.click(self.issues_locator)

    @allure.step("Click 'Cycles' link in sidebar")
    def click_cycles(self):
        self.click(self.cycles_locator)

    @allure.step("Check if teams management table is visible")
    def is_teams_management_table_present(self) -> bool:
        return self.is_element_present(self.teams_table_locator)
