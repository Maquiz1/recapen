# User Acceptance Testing (UAT) Template
**Project Name:** PEN-Plus Management System (RecaPen)
**Tester Name:** ________________________  
**Date:** ________________________  
**Role:** [ ] National/PI  [ ] Regional  [ ] District  [ ] Facility  [ ] Mentor

---

## Instructions
Please test each feature below by following the test steps. Mark the status as **Pass**, **Fail**, or **N/A** (Not Applicable for your role). If a test fails, provide details in the Comments/Defects section.

---

## 1. Authentication and Roles
| Test ID | Feature | Test Steps | Expected Result | Status (P/F/NA) | Comments |
|---------|---------|------------|-----------------|-----------------|----------|
| AUTH-01 | Login | Navigate to the login page and enter valid credentials. | User is successfully logged in and redirected to their respective dashboard. | | |
| AUTH-02 | Role Access | Log in as a Facility user and attempt to access National reports. | Access is denied or restricted. | | |
| AUTH-03 | Logout | Click the logout button from the Navbar. | User is securely logged out and returned to the login screen. | | |

## 2. Dashboards and Navigation
| Test ID | Feature | Test Steps | Expected Result | Status (P/F/NA) | Comments |
|---------|---------|------------|-----------------|-----------------|----------|
| DASH-01 | Dashboard Loading | Log in and view the default Admin dashboard. | Dashboard loads without errors. Charts and UI elements are visible. | | |
| DASH-02 | Medical Dashboard | Click "Medical Dashboard" on the sidebar. | The Medical Dashboard loads properly with correct layout and title. | | |
| DASH-03 | Clinic Dashboard | Click "Clinic Dashboard" on the sidebar. | The Clinic Dashboard loads properly with correct layout and title. | | |
| DASH-04 | Responsive UI | Resize the browser window to mobile width. | The sidebar collapses correctly and the layout remains usable. | | |

## 3. Patient Management (Upcoming Module)
| Test ID | Feature | Test Steps | Expected Result | Status (P/F/NA) | Comments |
|---------|---------|------------|-----------------|-----------------|----------|
| PAT-01 | Patient Registration | Navigate to 'Add Patient', fill in details, and save. | Patient is successfully saved in the database. | | |
| PAT-02 | Audit Trails | View a newly created patient record in the database/admin. | The `created_by` and `created_at` fields match the user and current time. | | |
| PAT-03 | Soft Deletion | Attempt to delete a patient record. | Record disappears from active views but is preserved in the database with `is_deleted=True`. | | |

## 4. Reports and Indicators (Upcoming Module)
| Test ID | Feature | Test Steps | Expected Result | Status (P/F/NA) | Comments |
|---------|---------|------------|-----------------|-----------------|----------|
| REP-01 | Generate Report | Select a date range and click "Generate Indicator Report". | Accurate data aggregates are displayed based on user's role constraints. | | |

---

## Tester Sign-off
**Overall Status:** [ ] Approved  [ ] Conditionally Approved (Pending fixes)  [ ] Rejected

**Tester Signature:** ___________________________  **Date:** _______________
