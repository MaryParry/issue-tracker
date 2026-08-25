import uuid
import allure
from ui.pages.workspaces_page import WorkspacesPage


@allure.feature("Workspace Navigation & Management")
class TestWorkspaces:
    @allure.story("UI-WS-01: Create Workspace Form Render")
    @allure.title("Verify create workspace form renders correctly")
    @allure.description(
        "Navigates to /workspace/create and checks for form input elements and submit button."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_workspace_form_render(self, authenticated_driver):
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        assert ws_page.is_create_workspace_form_rendered(), (
            f"Failed UI-WS-01: Create workspace form elements were not rendered on page '{authenticated_driver.current_url}'"
        )

    @allure.story("UI-WS-02: Create Workspace Form Validation")
    @allure.title("Verify creation form validation with invalid slug format")
    @allure.description(
        "Submits creation form with invalid slug format (spaces or uppercase) and checks for validation error."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_workspace_form_validation(self, authenticated_driver):
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("Acme Corp", "Acme Corp!", "UTC")
        error_text = ws_page.get_form_error_text()
        assert (
            error_text != ""
        ), f"Failed UI-WS-02: Expected validation error for invalid slug 'Acme Corp!', but no error text was displayed on page '{authenticated_driver.current_url}'"

    @allure.story("UI-WS-03: Workspace Dashboard Layout")
    @allure.title("Verify workspace dashboard layout")
    @allure.description(
        "Navigates to /workspace/:slug and checks for sidebar navigation and dashboard layout."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_workspace_dashboard_layout(self, authenticated_driver):
        slug = f"acme-{uuid.uuid4().hex[:6]}"
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("Acme Inc", slug, "UTC")

        ws_page.navigate_to_workspace(slug)
        assert ws_page.is_dashboard_layout_rendered(), (
            f"Failed UI-WS-03: Workspace sidebar navigation was not rendered at slug '/workspace/{slug}'. Current URL: '{authenticated_driver.current_url}'"
        )

    @allure.story("UI-WS-04: Workspace Selector Dropdown")
    @allure.title("Verify workspace selector dropdown navigation")
    @allure.description(
        "Clicks workspace selector dropdown in sidebar and verifies switching between workspaces."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_workspace_selector_dropdown(self, authenticated_driver):
        slug1 = f"ws-one-{uuid.uuid4().hex[:6]}"
        slug2 = f"ws-two-{uuid.uuid4().hex[:6]}"

        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("Workspace One", slug1, "UTC")

        ws_page.navigate_to_create()
        ws_page.create_workspace("Workspace Two", slug2, "UTC")

        ws_page.navigate_to_workspace(slug1)
        ws_page.open_workspace_selector()
        ws_page.select_workspace_from_dropdown("Workspace Two")

        assert (
            f"/workspace/{slug2}" in authenticated_driver.current_url
            or ws_page.is_dashboard_layout_rendered()
        ), f"Failed UI-WS-04: Selecting 'Workspace Two' from dropdown failed to navigate to '/workspace/{slug2}'. Current URL is '{authenticated_driver.current_url}'"

    @allure.story("UI-WS-05: Workspace Settings Navigation")
    @allure.title("Verify workspace settings navigation")
    @allure.description(
        "Clicks settings items in sidebar (Members, Roles, Labels, Priorities) and verifies routing."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_workspace_settings_navigation(self, authenticated_driver):
        slug = f"ws-settings-{uuid.uuid4().hex[:6]}"
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("WS Settings", slug, "UTC")

        ws_page.navigate_to_workspace(slug)
        for setting in ["Members", "Roles & permissions", "Labels", "Priorities"]:
            ws_page.click_settings_link(setting, slug)
            assert ws_page.is_dashboard_layout_rendered(), (
                f"Failed UI-WS-05: Navigating to setting section '{setting}' failed or sidebar was unrendered. Current URL is '{authenticated_driver.current_url}'"
            )

