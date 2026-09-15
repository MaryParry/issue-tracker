# Test Cases Specification

This document details the test strategy and test cases for **Prism Tracker**, covering both **API** procedures (oRPC / Elysia) and **UI** interactions (TanStack Router / Selenium).

---

## 1. API Test Cases

### 1.1 Workspaces (`workspaceRouter`)
| ID | Test Case | Description / Scenario | Input Data | Expected Result |
|---|---|---|---|---|
| **API-WS-01** | Create Workspace with valid input | User creates a workspace with a valid name, slug, and timezone. | `{ name: "Acme Corp", slug: "acme-corp", timezone: "UTC" }` | Returns created workspace object with cuid2 ID; seeds default issue statuses, priorities, built-in roles, default team, and workspace membership. |
| **API-WS-02** | Reject workspace creation with invalid slug | Slug contains invalid characters (e.g., spaces or uppercase). | `{ name: "Acme", slug: "Acme Corp!" }` | Validation error (`ZodError`): slug must match `/^[a-z0-9-]+$/`. |
| **API-WS-03** | Get Workspace by Slug | Authenticated user with `workspace:read` permission requests workspace by slug. | `{ slug: "acme-corp" }` | Returns workspace details matching slug. |
| **API-WS-04** | Get Workspace by Slug - Unauthorized / Not Found | User requests non-existent slug or lacks `workspace:read` permission. | `{ slug: "non-existent" }` | Throws `NOT_FOUND` error. |
| **API-WS-05** | Update Workspace | User with `workspace:update` permission updates workspace name. | `{ id: "ws-1", name: "Acme Updated" }` | Updates database record and returns updated workspace. |
| **API-WS-06** | Delete Workspace | User with `workspace:delete` permission deletes a workspace. | `{ id: "ws-1" }` | Workspace record removed from DB. |

---

### 1.2 Teams (`teamRouter`)
| ID | Test Case | Description / Scenario | Input Data | Expected Result |
|---|---|---|---|---|
| **API-TM-01** | Create Team | Create team within workspace using valid key and name. | `{ workspaceId: "ws-1", name: "Frontend Team", key: "FE" }` | Team created with `key` uppercased/validated against `/^[A-z0-9-]+$/`. Built-in team roles generated. |
| **API-TM-02** | Reject Invalid Team Key | Attempt to create team with illegal key (e.g., longer than 12 chars or invalid chars). | `{ workspaceId: "ws-1", name: "Engineering", key: "VERY_LONG_KEY_NAME" }` | Validation error: key max length 12 characters. |
| **API-TM-03** | List Teams for Workspace | Fetch all teams accessible to user in workspace. | `{ id: "ws-1" }` | Returns array of team objects. |

---

### 1.3 Issues (`issueRouter`)
| ID | Test Case | Description / Scenario | Input Data | Expected Result |
|---|---|---|---|---|
| **API-IS-01** | Create Issue | User with `issue:create` creates issue with title, team, and status. | `{ workspaceId: "ws-1", teamId: "team-1", statusId: "status-todo", title: "Fix header alignment" }` | Issue created with auto-incremented `number` for team, initial `sortOrder` lexorank, and activity logged (`issue.created`). |
| **API-IS-02** | Update Issue Title/Description | Update issue content. | `{ id: "issue-1", workspaceId: "ws-1", title: "Updated Title" }` | Updates fields, updates FTS/trigram search vectors, publishes `issue:changed` event. |
| **API-IS-03** | Move Issue Status (Lexorank Rebalancing) | Drag/move issue to new status column. | `{ id: "issue-1", workspaceId: "ws-1", statusId: "status-done" }` | Recalculates `sortOrder` at target status column top; triggers rebalance if ranks are exhausted. |
| **API-IS-04** | Parent Assignment - Hierarchy Validation | Assign a parent issue to create sub-issue. | `{ id: "sub-1", workspaceId: "ws-1", parentIssueId: "parent-1" }` | Validates parent belongs to same workspace & team. Checks tree depth <= 5. |
| **API-IS-05** | Parent Assignment - Prevent Loop | Attempt to set issue's parent to itself or a descendant. | `{ id: "parent-1", workspaceId: "ws-1", parentIssueId: "sub-1" }` | Throws `HIERARCHY_LOOP` error. |
| **API-IS-06** | Assign Closed Cycle Restriction | Attempt to assign issue to completed or canceled cycle. | `{ id: "issue-1", workspaceId: "ws-1", cycleId: "cycle-completed" }` | Throws `CYCLE_CLOSED` error. |

---

### 1.4 Cycles (`cycleRouter`)
| ID | Test Case | Description / Scenario | Input Data | Expected Result |
|---|---|---|---|---|
| **API-CY-01** | Create Cycle | Create cycle with start/end ISO date strings. | `{ workspaceId: "ws-1", teamId: "team-1", name: "Sprint 1", startDate: "2026-08-01T00:00:00Z", endDate: "2026-08-14T00:00:00Z" }` | Returns new cycle record in `upcoming` state. |
| **API-CY-02** | Cycle State Transition | Update cycle state from `upcoming` -> `active` -> `completed`. | `{ id: "cycle-1", workspaceId: "ws-1", state: "active" }` | Updates cycle state and records velocity metrics. |

---

## 2. UI Test Cases

### 2.1 Authentication & Auth Forms
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-AUTH-01** | Auth Form Render | Navigate to `/auth` route. | `/auth` | Displays email input, password input, sign-in button, and sign-up toggle link. |
| **UI-AUTH-02** | Toggle Sign-In / Sign-Up Mode | Click sign-up toggle link on `/auth`. | `/auth` | Toggles form heading and submit button text between "Sign in" and "Sign up". Shows name input when in sign-up mode. |
| **UI-AUTH-03** | Auth Input Validation | Enter invalid email format or password under 8 characters. | `/auth` | Prevents submission and displays inline field validation error message. |
| **UI-AUTH-04** | Invalid Credentials Error State | Submit invalid login credentials. | `/auth` | Displays top-level form error banner (`.form-error` / `FieldError`) with error message from auth service. |
| **UI-AUTH-05** | Invite Token Query Handling | Navigate to `/auth?inviteToken=abc-123`. | `/auth` | Preserves invite token and redirects user to `/invite/abc-123` upon successful authentication. |

---

### 2.2 Workspace Navigation & Management
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-WS-01** | Create Workspace Form Render | Navigate to `/workspace/create`. | `/workspace/create` | Displays workspace name input, workspace slug input, timezone input, and create workspace submission button. |
| **UI-WS-02** | Create Workspace Form Validation | Submit creation form with invalid slug format (e.g. spaces or uppercase). | `/workspace/create` | Displays field error indicating slug must match `/^[a-z0-9-]+$/`. |
| **UI-WS-03** | Workspace Dashboard Layout | Navigate to `/workspace/:slug`. | `/workspace/acme` | Displays workspace sidebar navigation (Issues, Cycles, Settings), team selector, and main content panel. |
| **UI-WS-04** | Workspace Selector Dropdown | Click workspace selector dropdown in sidebar. | `WorkspaceSidebar` | Displays list of user's workspaces; selecting a workspace navigates to `/workspace/:newSlug`. |
| **UI-WS-05** | Workspace Settings Navigation | Click settings items in sidebar (Members, Roles, Labels, Priorities). | `/workspace/:slug/settings/*` | Navigates to corresponding settings sub-route and updates active link state. |

---

### 2.3 Teams & Team Management
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-TM-01** | Team Sidebar Group Render | View workspace sidebar with active teams. | `WorkspaceSidebar` | Displays "Your teams" section with team names and default sub-items (Issues, Cycles). |
| **UI-TM-02** | Team Sub-Menu Navigation Routing | Click "Issues" or "Cycles" sub-link under team in sidebar. | `TeamSidebarMenuItem` | Navigates to `/workspace/:slug/teams/:teamSlug/issues` (or `/cycles`), loads team view, and sets active link highlight. |
| **UI-TM-03** | Manage Teams Action Link | Click gear icon next to "Your teams" in sidebar header. | `/workspace/:slug/teams` | Navigates to workspace team management route displaying list of workspace teams and create team action. |
| **UI-TM-04** | Create Team Modal Render | Click "+ Create team" button on teams page or sidebar header. | `TeamCreateModal` | Displays modal dialog containing team name input, team key input, and submit button. |
| **UI-TM-05** | Create Team Submission | Enter valid team name (e.g. "Frontend") and key (e.g. "FE"). | `TeamCreateForm` | Creates team, closes modal, and updates sidebar navigation and teams list with new team. |
| **UI-TM-06** | Create Team Key Validation | Enter invalid team key (e.g. >12 chars or illegal characters). | `TeamCreateForm` | Displays field error indicating key constraints (max 12 alphanumeric chars). |
| **UI-TM-07** | Team Cycle Settings | Navigate to team cycle settings route. | `/workspace/:slug/teams/:teamSlug/settings/cycles` | Renders controls to configure default cycle duration, auto-start, and auto-archive. |

---

### 2.4 Issue Board & Detail Views
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-IS-01** | Issue Board / List Route Render | Navigate to team issues page. | `/workspace/:slug/teams/:teamSlug/issues` | Displays status grouped columns (Backlog, Todo, In Progress, Done, Canceled), issue count badges, and header controls. |
| **UI-IS-02** | Toggle Kanban vs List View | Switch view mode toggle on issues page header. | `IssueViewHeader` | Toggles display layout between Kanban drag-and-drop board and compact table list view. |
| **UI-IS-03** | Create Issue Modal Render | Click "+ New issue" button or press keyboard shortcut. | `IssueCreateModal` | Renders issue modal with title input, markdown description editor, status, priority, assignee, cycle, issue type, and label selectors. |
| **UI-IS-04** | Create Issue Submission | Fill required title and select attributes, then click "Create issue". | `IssueCreateForm` | Creates issue, generates team key number (e.g., `FE-1`), closes modal, and appends issue card to target status column. |
| **UI-IS-05** | Create Issue Form Validation | Submit issue creation form with empty title. | `IssueCreateForm` | Prevents submission and displays inline validation error under title input field. |
| **UI-IS-06** | Kanban Drag & Drop Status Update | Drag an issue card from "Todo" to "In Progress" column. | `IssueBoardColumn` | Updates issue status in real-time, recalculates Lexorank sorting order, and triggers backend persistence. |
| **UI-IS-07** | Real-Time Issue Text Search | Enter search text into filter search bar. | `IssueFilters` | Filters visible issue cards dynamically based on title, description, or issue key match. |
| **UI-IS-08** | Filter Issues by Status / Priority / Label | Select specific filter criteria from filter popovers. | `IssueFilters` | Displays only issues matching all active filter parameters; shows active filter chips with clear buttons. |
| **UI-IS-09** | Grouping & Sorting Controls | Change group-by option (e.g., by Assignee or Priority) or sort order. | `IssueViewOptions` | Re-organizes board/list layout according to selected grouping field and sorting direction. |
| **UI-IS-10** | Issue Detail View Render | Navigate to specific issue detail route. | `/workspace/:slug/teams/:teamSlug/issue/:issueId` | Displays complete issue detail page with title, description, property bar, sub-issues section, and activity stream. |
| **UI-IS-11** | Edit Issue Title & Description | Click to edit title or description in detail view. | `IssueDetail` | Enables rich text editing, auto-saves on blur or save action, and updates issue header. |
| **UI-IS-12** | Update Meta Attributes via Property Bar | Change status, priority, assignee, cycle, estimate, or labels in detail view property bar. | `IssuePropertyBar` | Immediately updates issue metadata, logs activity change in timeline, and reflects across app. |
| **UI-IS-13** | Sub-Issue (Child) Hierarchy Management | Click "Add sub-issue" in issue detail view and link/create child issue. | `AddSubIssueDialog` | Links child issue, displays hierarchy tree with depth indicators (max 5 levels), and updates progress metrics. |
| **UI-IS-14** | Issue Comments & Activity Stream | Type a comment in activity section and click "Comment". | `IssueActivitySection` | Appends comment to discussion thread with user avatar, timestamp, and audit trail of attribute changes. |
| **UI-IS-15** | Delete Issue Action | Click issue action menu -> "Delete issue" and confirm deletion dialog. | `IssueDetailHeader` | Removes issue record, displays toast notification, and redirects user back to team issues list. |

---

### 2.5 Cycles & Sprint Planning
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-CY-01** | Cycle List Route Render | Navigate to team cycles page. | `/workspace/:slug/teams/:teamSlug/cycles/` | Displays tabs/sections for Active, Upcoming, and Completed cycles with date ranges and metrics. |
| **UI-CY-02** | Create Cycle Modal & Submission | Click "Create cycle", set cycle name, start date, and end date ISO strings. | `CycleFormDialog` | Validates dates, creates cycle record in "upcoming" state, and appends to cycles list. |
| **UI-CY-03** | Active Cycle Progress & Velocity Metrics | View active cycle card. | `CycleCard` / `CycleMetricsCard` | Renders burn-down progress bar, completed vs remaining issue points/count, and cycle end countdown. |
| **UI-CY-04** | Assign Issue to Active Cycle | Select cycle from issue property dropdown or drag issue into cycle. | `IssueCycleSelect` | Updates issue's cycle relationship and adjusts target cycle's scope and velocity calculations. |
| **UI-CY-05** | Cycle State Transition & Complete Cycle Dialog | Click "Complete cycle" action on an active cycle. | `CycleCompleteDialog` | Prompts user to handle uncompleted issues (move to next cycle or backlog) and transitions state to "completed". |

---

### 2.6 Command Palette & Navigation Shortcuts
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-CMD-01** | Command Palette Render | Press `Cmd+K` / `Ctrl+K` keyboard shortcut or click search icon. | `SearchPaletteDialog` | Opens overlay search modal with input field and categorized action/navigation commands. |
| **UI-CMD-02** | Command Palette Search & Navigation | Type query (e.g. issue key, team name, setting) and press Enter. | `SearchPalette` | Filters commands and issues in real-time; selecting an item navigates immediately to target route. |

---

### 2.7 Workspace Settings & Administration
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-SET-GEN-01** | General Workspace Settings Render & Update | Navigate to `/workspace/:slug/settings/general`. | `WorkspaceSettingsGeneral` | Displays workspace name, slug, timezone, icon upload; saving updates workspace properties. |
| **UI-SET-GEN-02** | Workspace Deletion Flow | Scroll to Danger Zone in general settings and confirm slug deletion prompt. | `WorkspaceSettingsGeneral` | Deletes workspace and all associated resources; redirects user to workspace creation page. |
| **UI-SET-MEM-01** | Workspace Members List View | Navigate to `/workspace/:slug/settings/members`. | `WorkspaceMembersView` | Displays table of workspace members, email addresses, assigned workspace roles, and pending invites. |
| **UI-SET-MEM-02** | Invite Workspace Member | Click "Invite member", enter recipient email address, and select initial role. | `InviteMemberModal` | Creates pending invitation record, generates invite token link, and shows success toast. |
| **UI-SET-MEM-03** | Change Member Role & Revoke Membership | Select role dropdown for existing member or click "Remove member". | `WorkspaceMembersView` | Updates user permissions immediately or removes member from workspace upon confirmation. |
| **UI-SET-ROL-01** | Roles & Permissions Matrix Render | Navigate to `/workspace/:slug/settings/roles`. | `WorkspaceRolesView` | Displays built-in (Owner, Admin, Member) and custom roles with granular permission matrix toggles. |
| **UI-SET-ROL-02** | Create & Edit Custom Role | Click "Create role", enter role name/description, and select permission flags. | `WorkspaceRoleModal` | Saves custom role, displays in role list, and makes role assignable to workspace members. |
| **UI-SET-WF-01** | Workflow Statuses Management View | Navigate to `/workspace/:slug/settings/workflow`. | `IssueStatusesView` | Displays status categories (Backlog, Todo, In Progress, Done, Canceled) and current workflow statuses. |
| **UI-SET-WF-02** | Create Custom Workflow Status | Click "Add status", enter name, pick color, and select state group. | `StatusCreateModal` | Adds new status to state category, makes status selectable in issues, and updates board columns. |
| **UI-SET-LBL-01** | Labels List & Create Modal | Navigate to `/workspace/:slug/settings/labels`. | `LabelList` | Displays list of workspace labels with color badges; "Create label" modal permits adding label with hex color. |
| **UI-SET-LBL-02** | Edit & Delete Label | Click edit/delete icon on label row. | `LabelFormModal` | Updates label name/color or removes label with confirmation dialog. |
| **UI-SET-PRI-01** | Priorities Management View | Navigate to `/workspace/:slug/settings/priorities`. | `IssuePrioritiesView` | Displays system and custom priority levels (Urgent, High, Medium, Low, None) with order and color controls. |
| **UI-SET-TYP-01** | Issue Types Management View | Navigate to `/workspace/:slug/settings/issue-types`. | `IssueTypesView` | Displays list of issue types (Task, Bug, Feature, Improvement); permits creating/editing issue type name and icon. |

---

### 2.8 Workspace Invitations & Member Onboarding
| ID | Test Case | Description / Scenario | Target Route / Component | Expected Result |
|---|---|---|---|---|
| **UI-INV-01** | Invite Token Link Page Render | Navigate to `/invite/:token` as authenticated user. | `/invite/$token` | Renders invitation details page showing workspace name, inviter name, and "Accept Invitation" button. |
| **UI-INV-02** | Accept Invitation Flow | Click "Accept Invitation" button on invite page. | `/invite/$token` | Grants workspace membership, redirects user to `/workspace/:slug`, and displays success toast. |
| **UI-INV-03** | Invalid or Expired Token Error State | Navigate to `/invite/invalid-token-code`. | `/invite/$token` | Renders clear error message banner stating invitation link is invalid or expired with link to home. |

---

## 3. Automation Test Suite Execution

- **API Unit Tests**: Executed via Bun Test: `nix develop --command bun test packages/api`
- **UI Unit Tests**: Executed via Vitest: `nix develop --command bun -F tss-web test:unit`
- **UI E2E Selenium Tests**: Executed via PyTest: `nix develop --command pytest tests/ui`

