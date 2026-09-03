import uuid
import allure
import pytest
from ui.pages.teams_page import TeamsPage
from ui.pages.workspaces_page import WorkspacesPage


@pytest.fixture
def teams_page(authenticated_driver):
    """Sets up a workspace and returns an initialized TeamsPage on that workspace."""
    slug = f"team-ws-{uuid.uuid4().hex[:6]}"
    ws_page = WorkspacesPage(authenticated_driver)
    ws_page.navigate_to_create()
    ws_page.create_workspace("Team Workspace", slug, "UTC")
    ws_page.navigate_to_workspace(slug)
    return TeamsPage(authenticated_driver)


@allure.feature("Teams & Team Navigation")
class TestTeams:
    @allure.story("UI-TM-01: Team Sidebar Group Render")
    @allure.title("Verify team sidebar group renders correctly")
    @allure.description(
        "Navigates to workspace dashboard and checks for 'Your teams' section."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_team_sidebar_group_render(self, teams_page):
        assert teams_page.is_default_team_present(), (
            "Failed UI-TM-01: default team is not present"
        )
        assert teams_page.is_cycles_link_present(), (
            "Failed UI-TM-01: Cycles element is not present"
        )
        assert teams_page.is_issues_link_present(), (
            "Failed UI-TM-01: Issues link is not present"
        )

    @allure.story("UI-TM-02: Toggle Team Sidebar Menu")
    @allure.title("Verifies Team Toggle and its sub-elements working correctly")
    @allure.description(
        "Clicks on My Teams, Ensures toggle works correctly and that all the sub-elements route accordingly"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_team_subelement_toggle_routing(self, teams_page):
        teams_page.click_default_team()
        assert not (
            teams_page.is_issues_link_present() and teams_page.is_cycles_link_present()
        ), "Failed UI-TM-02: The Toggle did not render sub-elements"

        assert not teams_page.get_url().split("/")[-1] == "cycles", (
            "Failed UI-TM-02: Could not route to cycles"
        )
        assert "issue" not in teams_page.get_url(), (
            "Failed UI-TM-02: Could not route to issue"
        )
        teams_page.click_default_team()
        assert (
            teams_page.is_issues_link_present() and teams_page.is_cycles_link_present()
        ), "Failed UI-TM-02: The Toggle did not render sub-elements"

        teams_page.click_cycles()
        assert teams_page.get_url().split("/")[-1] == "cycles", (
            "Failed UI-TM-02: Could not route to cycles"
        )
        teams_page.click_issues()
        assert "issue" in teams_page.get_url(), (
            "Failed UI-TM-02: Could not route to issue"
        )

    @allure.story("UI-TM-03: Manage Teams Action Link")
    @allure.title("Verifies Gear Icon's functionality next to 'Your teams'")
    @allure.description(
        "Navigates to workspace team management route displaying list of workspace teams and create team action"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_your_teams_gear_btn(self, teams_page):
        teams_page.click(teams_page.manage_teams_locator)

        assert teams_page.is_teams_management_table_present(), (
            "Failed UI-TM-04: Teams Table is not visible"
        )

    @allure.story("UI-TM-04: Create Team Modal Render")
    @allure.title("Verifies Team creation Form Render")
    @allure.description(
        "Clicks on 'Create Team' Button in 'Your Teams' Section and checks for form's elements render"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_team_modal_render(self, teams_page):
        teams_page.click(teams_page.manage_teams_locator)
        teams_page.click_create_team()

        assert teams_page.is_create_team_form_rendered(), (
            "Failed UI-TM-04: Create Team modal and form elements did not render"
        )
        assert teams_page.is_color_picker_present(), (
            "Failed UI-TM-04: Color picker is not present in Create Team modal"
        )
        assert teams_page.is_cycle_duration_present(), (
            "Failed UI-TM-04: Cycle duration control is not present in Create Team modal"
        )

    @allure.story("UI-TM-05: Create Team Submission")
    @allure.title("Verify creating a team with valid name and key")
    @allure.description(
        "Fills in valid team name and key, submits the form, and verifies modal closes, "
        "team appears in the management table, and team appears in sidebar navigation."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_team_submission(self, teams_page):
        teams_page.click_manage_teams()
        teams_page.click_create_team()
        assert teams_page.is_create_team_modal_open(), (
            "Failed UI-TM-05: Create Team modal is not open"
        )

        team_name = f"Frontend Team {uuid.uuid4().hex[:4]}"
        team_key = f"FE{uuid.uuid4().hex[:2].upper()}"

        teams_page.create_team(team_name, team_key)

        assert teams_page.is_create_team_modal_closed(), (
            "Failed UI-TM-05: Create team modal did not close after submission"
        )
        assert teams_page.is_team_in_teams_table(team_name), (
            f"Failed UI-TM-05: Team '{team_name}' was not found in teams management table"
        )
        assert teams_page.is_team_in_teams_table(team_key), (
            f"Failed UI-TM-05: Team key '{team_key}' was not found in teams management table"
        )
        assert teams_page.is_team_in_sidebar(team_name), (
            f"Failed UI-TM-05: Team '{team_name}' was not found in sidebar navigation"
        )

    @allure.story("UI-TM-06: Create Team Key Validation")
    @allure.title("Verify team key validation on team creation form")
    @allure.description(
        "Submits team creation form with an invalid key (>12 chars or illegal characters) "
        "and verifies field validation error is displayed and modal remains open."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_team_key_validation(self, teams_page):
        teams_page.click_manage_teams()
        teams_page.click_create_team()
        assert teams_page.is_create_team_modal_open(), (
            "Failed UI-TM-06: Create Team modal is not open"
        )

        invalid_key = "TOOLONGKEY12345"
        teams_page.create_team("Invalid Key Team", invalid_key)

        error_text = teams_page.get_key_field_error()
        assert error_text != "" or teams_page.is_key_field_invalid(), (
            "Failed UI-TM-06: Expected validation error for invalid key, but no error was displayed"
        )
        assert teams_page.is_create_team_modal_open(), (
            "Failed UI-TM-06: Modal should remain open when form validation fails"
        )



