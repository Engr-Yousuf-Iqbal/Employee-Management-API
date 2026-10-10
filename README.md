# Employee Management API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-REST%20API-black)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)

A RESTful Employee Management API built with Python, Flask, SQLAlchemy, and PostgreSQL. The project implements JWT authentication, role-based access control (RBAC), employee management, audit logging, database migrations, automated testing, Docker containerization, and a GitHub Actions continuous integration pipeline.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [User Roles and Permissions](#user-roles-and-permissions)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Docker Setup](#docker-setup)
- [Testing and Coverage](#testing-and-coverage)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Security Considerations](#security-considerations)
- [Future Improvements](#future-improvements)

## Features

### Authentication and Authorization
- User registration and login.
- JWT-based access and refresh tokens.
- Password hashing.
- Protected API endpoints.
- Role-based access control for Admin, Manager, and Employee roles.
- Authenticated user profile endpoint.

### Employee Management
- Create, retrieve, update, and delete employee records.
- Associate employee records with user accounts.
- Restrict employees to accessing and updating their own records.
- Support administrative and managerial access according to role permissions.
- Validate incoming request data.

### API Features
- Versioned API routes using `/api/v1/`.
- Pagination for employee listings.
- Employee search and filtering.
- Centralized error handling.
- Swagger API documentation through Flasgger.

### Audit Logging and Security
- Audit events for selected operations, including authentication and employee/user changes.
- Administrative access to audit-log endpoints.
- Rate limiting with Flask-Limiter.
- Configuration through environment variables.

### Database and DevOps
- PostgreSQL integration using Flask-SQLAlchemy.
- Version-controlled database schema changes using Flask-Migrate and Alembic.
- Automated tests using pytest.
- Test coverage reports using pytest-cov.
- Docker image for the Flask API.
- Docker Compose for running the API and PostgreSQL together.
- Persistent PostgreSQL storage through a Docker volume.
- GitHub Actions workflow for automated testing, coverage, and Docker image builds.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python 3.12 |
| Backend | Flask, REST APIs |
| ORM | Flask-SQLAlchemy, SQLAlchemy |
| Database | PostgreSQL |
| Authentication | Flask-JWT-Extended, JWT |
| API Documentation | Flasgger, Swagger/OpenAPI |
| Security | RBAC, password hashing, Flask-Limiter |
| Migrations | Flask-Migrate, Alembic |
| Testing | pytest, pytest-cov |
| API Testing | Postman |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions, YAML |
| Version Control | Git, GitHub |

## Architecture

The application follows a layered structure to separate routing, business logic, data access, and database models.

```text
Client / Postman
       |
       v
Flask Routes
       |
       v
Controllers
       |
       v
Services
       |
       v
Repositories
       |
       v
SQLAlchemy Models
       |
       v
PostgreSQL
```

Supporting components include:

- **Middleware:** request protection and error handling.
- **Schemas:** request validation and data serialization, where implemented.
- **Utilities:** reusable application helpers.
- **Audit logging:** records selected application events.
- **Flask-Migrate/Alembic:** manages database schema revisions.
- **Docker Compose:** runs the API and database as separate services.

## User Roles and Permissions

| Operation | Admin | Manager | Employee |
|---|---|---|---|
| Create employee | Yes | Yes | No |
| View all employees | Yes | Yes | No |
| View individual employee | Yes | Yes | Own record |
| Update employee | Yes | Yes | Own record |
| Delete employee | Yes | No | No |
| Access administrative audit logs | Yes | No | No |

Access is enforced by the application's authorization logic. Exact permissions depend on the route and its configured decorators.

## API Endpoints

Base URL for local development:

`http://127.0.0.1:5000`

### Authentication and Users

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/users/register` | Register a user |
| POST | `/api/v1/users/login` | Authenticate a user, if configured on this route |
| GET | `/api/v1/users/me` | Retrieve the authenticated user's profile |
| POST | `/api/v1/auth/refresh` | Refresh an access token |

### Employees

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/employees` | Create an employee |
| GET | `/api/v1/employees` | Retrieve employee records |
| GET | `/api/v1/employees/{employee_id}` | Retrieve an employee by ID |
| PUT | `/api/v1/employees/{employee_id}` | Update an employee |
| DELETE | `/api/v1/employees/{employee_id}` | Delete an employee |

Employee listing supports pagination and configured search/filter parameters.

### Audit Logs

Audit-log endpoints are available to authorized administrators. Refer to the registered audit routes and Swagger documentation for the exact paths and supported query parameters.

> Verify the authentication route paths against your current Flask blueprints before publishing this endpoint table. The table documents the intended API surface, and route registrations in the code are authoritative.

## Getting Started

### Prerequisites

For local development:

- Python 3.12
- PostgreSQL
- Git
- Postman (recommended)

For containerized development:

- Docker Desktop
- Docker Compose

### 1. Clone the Repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone <your-repository-url>
cd employee-management-api
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the appropriate execution policy for your environment or activate the environment through VS Code.

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root. Use the appropriate database URL for your chosen execution mode.

For local execution:

```env
FLASK_ENV=development

SECRET_KEY=replace-with-a-development-secret
JWT_SECRET_KEY=replace-with-a-development-jwt-secret

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/employee_management

JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

Replace `YOUR_PASSWORD` with your PostgreSQL password. URL-encode special characters in the database URL when necessary.

Ensure that the database exists and that the configured user has the required permissions.

### 5. Run Database Migrations

Apply the existing migration history:

```powershell
python -m flask --app run.py db upgrade
```

Check the current revision:

```powershell
python -m flask --app run.py db current
```

### 6. Start the Application

```powershell
python run.py
```

The API should be available at:

`http://127.0.0.1:5000`

Swagger documentation:

`http://127.0.0.1:5000/apidocs/`

## Environment Variables

| Variable | Purpose |
|---|---|
| `FLASK_ENV` | Selects the configured application environment |
| `SECRET_KEY` | Flask application secret |
| `JWT_SECRET_KEY` | Signs JWT tokens |
| `DATABASE_URL` | SQLAlchemy database connection |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access-token lifetime in seconds |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh-token lifetime in seconds |

Keep `.env` out of version control. Never commit production credentials or secret keys.

## Database Migrations

The project uses Flask-Migrate and Alembic to manage database schema changes.

### Generate a Migration

After modifying a model:

```powershell
python -m flask --app run.py db migrate -m "Describe schema change"
```

Review the generated migration before applying it.

### Apply Migrations

```powershell
python -m flask --app run.py db upgrade
```

### Inspect Migration History

```powershell
python -m flask --app run.py db history
python -m flask --app run.py db current
```

### Roll Back a Revision

```powershell
python -m flask --app run.py db downgrade
```

Use downgrade only after reviewing the migration and understanding its effect on existing data.

**Workflow:** update model → generate migration → review migration → apply migration.

## Docker Setup

Docker Compose runs the Flask API and PostgreSQL as separate services.

### Start the Services

From the project root:

```powershell
docker compose up -d --build
```

Check their status:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs -f
```

### Configure the Container Database

Inside Docker Compose, the API must connect to the database using the Compose service name, typically `db`, rather than `localhost`.

Example connection URL:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db:5432/employee_management
```

The PostgreSQL credentials in `docker-compose.yml` must match the credentials in the database URL. Keep passwords consistent between the service configuration and application environment.

### Apply Migrations in Docker

```powershell
docker compose exec api flask --app run.py db upgrade
```

Check the migration revision:

```powershell
docker compose exec api flask --app run.py db current
```

### Stop the Services

```powershell
docker compose down
```

PostgreSQL data is stored in the configured named volume and persists when containers are stopped or recreated.

To remove the containers and their associated volumes:

```powershell
docker compose down -v
```

**Warning:** this deletes the Compose-managed database volume and its stored data. Do not run it unless that data can be discarded.

## Testing and Coverage

The project uses pytest for automated testing and pytest-cov for coverage reporting.

### Run Tests

```powershell
python -m pytest -v
```

### Generate a Coverage Summary

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

### Generate an HTML Coverage Report

```powershell
python -m pytest --cov=app --cov-report=html
```

Open `htmlcov/index.html` in a browser to inspect the report.

The test suite covers authentication, users, employees, and audit logging. Tests use an isolated test database configured through the test fixtures.

## CI/CD Pipeline

The project uses **GitHub Actions** to automate continuous integration.

Workflow file:

`.github/workflows/ci.yml`

The workflow is configured to run on pushes to `main` and pull requests targeting `main`.

### Pipeline Steps

1. Check out the repository.
2. Set up Python 3.12.
3. Install project dependencies from `requirements.txt`.
4. Start a PostgreSQL service for CI, where configured.
5. Run the pytest suite.
6. Generate a test coverage report.
7. Build the Docker image after the test job succeeds.

### Pipeline Flow

```text
Git Push / Pull Request
          |
          v
    GitHub Actions
          |
          v
 Install Dependencies
          |
          v
      Run Tests
          |
          v
   Generate Coverage
          |
          v
   Build Docker Image
          |
          v
    CI Result: PASS/FAIL
```

A failed test job prevents the dependent Docker build job from running.

The workflow uses test credentials and must not depend on your local `.env` file or production secrets.

### Check Workflow Results

1. Open the GitHub repository.
2. Select the **Actions** tab.
3. Open the `Employee Management API CI` workflow.
4. Inspect the job logs if a step fails.

### CI Badge

```markdown
![CI](https://github.com/ENGR-Yousuf-Iqbal/Employee-Management-API/actions/workflows/ci.yml/badge.svg)
```

## API Documentation

Swagger documentation is provided by Flasgger.

When the local application is running, open:

`http://127.0.0.1:5000/apidocs/`

Use the documentation to inspect available routes, parameters, request bodies, and response formats. Protected endpoints require valid authentication and appropriate permissions.

## Project Structure

```text
employee-management-api/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── config/
│   ├── controllers/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── migrations/
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_user.py
│   ├── test_employee.py
│   └── test_audit.py
│
├── .dockerignore
├── .env                  # Local only; do not commit
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── run.py
```

## Security Considerations

- Store secrets and credentials in environment variables.
- Never commit `.env` or production credentials.
- Use strong, unique secret keys outside local development.
- Enforce authorization on protected endpoints.
- Use password hashing rather than storing plaintext passwords.
- Review generated migrations before applying them.
- Configure a persistent, shared rate-limit storage backend such as Redis before production use.
- Use HTTPS and production-appropriate server configuration when deploying.
- Configure database backups and restrict database access in production.

## Future Improvements

- Deploy the API to a cloud platform or VPS.
- Add production secret management and environment-specific configuration.
- Configure persistent rate-limit storage.
- Expand integration tests and enforce an appropriate coverage threshold.
- Add automated deployment to the CI/CD pipeline.
- Improve monitoring, logging, and operational documentation.

## License

No license has been specified yet. Add a `LICENSE` file if you intend to publish this project with explicit reuse permissions.
