import uuid
import allure
from ui.pages.teams_page import TeamsPage
from ui.pages.workspaces_page import WorkspacesPage


@allure.feature("Teams & Team Navigation")
class TestTeams:
    @allure.story("UI-TM-01: Team Sidebar Group Render")
    @allure.title("Verify team sidebar group renders correctly")
    @allure.description(
        "Navigates to workspace dashboard and checks for 'Your teams' section."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_team_sidebar_group_render(self, authenticated_driver):
        slug = f"team-ws-{uuid.uuid4().hex[:6]}"
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("Team Workspace", slug, "UTC")
        ws_page.navigate_to_workspace(slug)

        teams_page = TeamsPage(authenticated_driver)
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
    def test_team_subelement_toggle_routing(self, authenticated_driver):
        slug = f"team-ws-{uuid.uuid4().hex[:6]}"
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("Team Workspace", slug, "UTC")
        ws_page.navigate_to_workspace(slug)

        teams_page = TeamsPage(authenticated_driver)

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
    def test_your_teams_gear_btn(self, authenticated_driver):
        slug = f"team-ws-{uuid.uuid4().hex[:6]}"
        ws_page = WorkspacesPage(authenticated_driver)
        ws_page.navigate_to_create()
        ws_page.create_workspace("Team Workspace", slug, "UTC")
        ws_page.navigate_to_workspace(slug)

        teams_page = TeamsPage(authenticated_driver)
        teams_page.click(teams_page.manage_teams_locator)

        assert teams_page.is_teams_management_table_present(), (
            "Failed UI-TM-04: Teams Table is not visible"
        )
