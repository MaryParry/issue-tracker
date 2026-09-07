import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

        self.settings_locator = (
            By.XPATH,
            "//a[contains(@href, '/teams') and .//span[normalize-space()='Manage teams']]",
        )

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
        self.create_team_key_error_locator = (
            By.XPATH,
            "//div[@role='dialog']//input[@id='key']/ancestor::div[@data-slot='field']//*[@data-slot='field-error'] | //div[@role='dialog']//*[@data-slot='field-error']",
        )
        self.create_team_key_invalid_input_locator = (
            By.CSS_SELECTOR,
            'div[role="dialog"] input#key[aria-invalid="true"]',
        )

        # Team Cycle Settings Locators (UI-TM-07)
        self.team_cycle_settings_link = (
            By.XPATH,
            "//table[@data-slot='table']//a[normalize-space()='Cycle settings'] | //a[contains(@href, '/settings/cycles')]",
        )
        self.cycle_settings_heading = (
            By.XPATH,
            "//h1[contains(normalize-space(), 'cycle settings')]",
        )
        self.cycle_settings_card_title = (
            By.XPATH,
            "//*[contains(concat(' ', normalize-space(@class), ' '), ' card-title ') or self::h3][normalize-space()='Cycle automation'] | //*[normalize-space()='Cycle automation']",
        )
        self.cycle_settings_back_link = (
            By.XPATH,
            "//a[contains(normalize-space(), 'Teams') and contains(@href, '/teams')]",
        )
        self.cycle_settings_cadence_switch = (By.ID, "cadence-enabled")
        self.cycle_settings_cadence_days_input = (By.ID, "cadence-days")
        self.cycle_settings_anchor_date_input = (By.ID, "anchor-date")
        self.cycle_settings_planning_horizon_input = (By.ID, "planning-horizon")
        self.cycle_settings_end_behavior_select = (By.ID, "end-behavior")
        self.cycle_settings_grace_period_input = (By.ID, "grace-period")
        self.cycle_settings_default_rollover_select = (By.ID, "default-rollover")
        self.cycle_settings_reminder_lead_input = (By.ID, "reminder-lead")
        self.cycle_settings_preview_section = (
            By.CSS_SELECTOR,
            "section[aria-label='Schedule preview']",
        )
        self.cycle_settings_submit_btn = (
            By.CSS_SELECTOR,
            "form button[type='submit']",
        )

        # Issues page locators

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

    @allure.step("Click 'Manage teams' link in sidebar")
    def click_manage_teams(self):
        self.click(self.manage_teams_locator)

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

    @allure.step("Enter team name '{name}'")
    def enter_team_name(self, name: str):
        field = self.find(self.create_team_form_name)
        field.clear()
        field.send_keys(name)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            field,
        )

    @allure.step("Enter team key '{key}'")
    def enter_team_key(self, key: str):
        field = self.find(self.create_team_form_key)
        field.clear()
        field.send_keys(key)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            field,
        )

    @allure.step("Click submit button in create team modal")
    def submit_create_team(self):
        self.click(self.create_team_submit_btn)

    @allure.step("Create team with name '{name}' and key '{key}'")
    def create_team(self, name: str, key: str):
        self.enter_team_name(name)
        self.enter_team_key(key)
        self.submit_create_team()

    @allure.step("Check if create team modal is closed")
    def is_create_team_modal_closed(self, timeout=10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.create_team_modal_locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    @allure.step(
        "Check if team '{team_name_or_key}' is present in teams management table"
    )
    def is_team_in_teams_table(self, team_name_or_key: str, timeout=10) -> bool:
        locator = (
            By.XPATH,
            f"//table[@data-slot='table']//td[contains(normalize-space(), '{team_name_or_key}')]",
        )
        return self.is_element_present(locator, timeout=timeout)

    @allure.step("Check if team '{team_name}' is present in sidebar")
    def is_team_in_sidebar(self, team_name: str, timeout=10) -> bool:
        locator = (
            By.XPATH,
            f"//aside[contains(@data-slot, 'sidebar') or contains(@data-sidebar, 'sidebar')]//span[normalize-space()='{team_name}'] | //span[normalize-space()='{team_name}']",
        )
        return self.is_element_present(locator, timeout=timeout)

    @allure.step("Get key field validation error text")
    def get_key_field_error(self, timeout=5) -> str:
        if self.is_element_present(self.create_team_key_error_locator, timeout=timeout):
            return self.get_text(self.create_team_key_error_locator, timeout=timeout)
        return ""

    @allure.step("Check if key field is marked invalid")
    def is_key_field_invalid(self, timeout=5) -> bool:
        return self.is_element_present(
            self.create_team_key_invalid_input_locator, timeout=timeout
        )

    @allure.step("Click sidebar teams settings")
    def click_sidebar_settings(self):
        return self.click(self.settings_locator)

    @allure.step("Click Cycle Settings")
    def click_cycle_settings(self):
        return self.click(self.team_cycle_settings_link)
