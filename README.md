# PEN-Plus Management System (RecaPen)

A comprehensive, role-based management system designed for the PEN-Plus initiative, ultimately transitioning to the Ministry of Health. This system tracks patients, indicators, and hospital/clinic metrics across National, Regional, District, and Facility levels.

## Features

- **Role-Based Access Control:** Custom User models supporting hierarchical roles (National, Regional, District, Facility, Mentor, PI).
- **Beautiful Dashboards:** Powered by the Apollo Medical Admin Template, featuring modular UI components (Sidebar, Navbar, Footer).
- **Auditable Records:** Every database entry automatically tracks creation and modification timestamps, alongside the responsible user, utilizing soft-delete mechanisms.
- **Scalable Architecture:** Built with Django and PostgreSQL, ensuring robust performance and security.

## Technology Stack

- **Backend:** Python 3.10, Django 4.2
- **Database:** PostgreSQL (with `django-environ` for configuration)
- **Frontend:** HTML, CSS, JavaScript (Apollo Medical Admin Template)

## Setup & Installation

1. **Virtual Environment:**
   ```bash
   python3 -m venv venv-recapen
   source venv-recapen/bin/activate
   ```

2. **Dependencies:**
   ```bash
   pip install django django-environ psycopg2-binary
   ```

3. **Database Configuration:**
   Ensure PostgreSQL is running and you have a `.env` file in the `backend/config/` directory with:
   ```env
   DB_NAME=recapen_db
   DB_USER=postgres
   DB_PASSWORD=Data@2026
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **Run Migrations & Server:**
   ```bash
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```

## Documentation

- [User Manual](docs/User_Manual.md)
- [Technical Manual](docs/Technical_Manual.md)
- [Presentation](docs/User_Presentation.md)
