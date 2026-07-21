# PEN-Plus Management System: Technical Manual

This document outlines the architecture, data models, and UI structure of the PEN-Plus Management System backend.

## 1. Architecture Overview

The system is built as a modular Django project consisting of several distinct apps:
- `core`: Contains base models and shared utilities.
- `accounts`: Handles authentication, user models, and role-based access.
- `dashboards`: Manages the UI, templates, and dashboard views.
- `reports`: (Upcoming) Will handle data aggregation and indicator reporting.
- `patients`: (Upcoming) Will manage the patient registry.

## 2. Data Models

### Custom User Model (`accounts.CustomUser`)
We use a custom user model replacing Django's default `User`. It extends `AbstractUser` and includes:
- `phone_number`: Optional contact field.
- `role_type`: A categorical choice field defining the hierarchy (National, Regional, District, Facility, Mentor, PI).

### Auditable Model (`core.AuditableModel`)
An abstract base class that ensures strict tracking. All major models in the system should inherit from this.
Fields provided:
- `created_at` / `updated_at`: Timestamps.
- `created_by` / `updated_by`: Foreign keys to `CustomUser`.
- `is_deleted` / `deleted_at`: Soft-delete mechanism to preserve historical data integrity.

## 3. UI and Templating

The frontend utilizes the **Apollo Medical Admin Template**. We have refactored this template into a DRY (Don't Repeat Yourself) Django template structure:

### Base Layout (`backend/templates/base.html`)
The master template that includes the global CSS/JS, and defines `{% block content %}` and `{% block page_title %}`.

### Partials (`backend/templates/includes/`)
- `sidebar.html`: The left-side navigation menu.
- `navbar.html`: The top header and search bar.
- `footer.html`: Global copyright footer.

### Static Assets
Static files (CSS, JS, SVG icons, images) are located in `backend/static/assets/`. Django's `STATICFILES_DIRS` is configured to serve them globally.

## 4. Database Setup

The project uses **PostgreSQL** configured via `django-environ`.
- **Database Name:** `recapen_db`
- **User:** `postgres`

Ensure environment variables (`DATABASE_URL` or explicit DB variables) are present in the `.env` file before running migrations.
