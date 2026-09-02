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
        self.manage_teams_locator = (
            By.XPATH,
            "//a[contains(@href, '/teams') and .//span[normalize-space()='Manage teams']]",
        )

        # Your Teams Locators
        self.teams_table_locator = (By.CSS_SELECTOR, 'table[data-slot="table"]')

        # Create Team Form Locators
        self.create_team_modal_locator = (By.CSS_SELECTOR, 'div[role="dialog"]')
        self.create_team_locator = (
            By.XPATH,
            "//button[normalize-space()='Create team']",
        )
        self.create_team_form_name = (By.ID, "name")
        self.create_team_form_key = (By.ID, "key")
        self.create_team_color_picker_trigger = (
            By.XPATH,
            "//div[@role='dialog']//button[.//svg[contains(@class, 'lucide-pipette')]] | //div[@role='dialog']//label[normalize-space()='Color']/..//button[1]",
        )
        self.create_team_random_color_btn = (
            By.XPATH,
            "//div[@role='dialog']//button[.//svg[contains(@class, 'lucide-refresh-ccw')]]",
        )
        self.create_team_preset_colors = (
            By.XPATH,
            "//div[@role='dialog']//div[contains(@class, 'overflow-x-auto')]//button",
        )
        self.create_team_cycle_duration_select = (
            By.XPATH,
            "//div[@role='dialog']//label[normalize-space()='Cycle duration']/../..//button[@role='combobox'] | //div[@role='dialog']//button[@role='combobox']",
        )
        self.create_team_submit_btn = (
            By.CSS_SELECTOR,
            'div[role="dialog"] button[type="submit"]',
        )

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

    @allure.step("Click 'Create Team' button")
    def click_create_team(self):
        return self.click(self.create_team_locator)

    @allure.step("Check if Create Team modal is open")
    def is_create_team_modal_open(self) -> bool:
        return self.is_element_present(self.create_team_modal_locator)

    @allure.step("Check if color picker is present in create team form")
    def is_color_picker_present(self) -> bool:
        return self.is_element_present(self.create_team_color_picker_trigger)

    @allure.step("Check if cycle duration control is present in create team form")
    def is_cycle_duration_present(self) -> bool:
        return self.is_element_present(self.create_team_cycle_duration_select)

    @allure.step("Check if create team modal and form controls are rendered")
    def is_create_team_form_rendered(self) -> bool:
        return (
            self.is_create_team_modal_open()
            and self.is_element_present(self.create_team_form_name)
            and self.is_element_present(self.create_team_form_key)
            and self.is_color_picker_present()
            and self.is_cycle_duration_present()
            and self.is_element_present(self.create_team_submit_btn)
        )
