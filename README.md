# Employee Management API

A production-oriented RESTful Employee Management API built with **Python, Flask, SQLAlchemy, PostgreSQL, JWT authentication, RBAC, and layered architecture**.

The project demonstrates backend API development practices including authentication, authorization, CRUD operations, validation, pagination, filtering, search, API versioning, automated testing, and OpenAPI/Swagger documentation.

---

## 1. Project Overview

The Employee Management API provides a secure backend system for managing employee records and user accounts.

The API separates responsibilities into different layers:

```text
Client
  │
  ▼
Routes
  │
  ▼
Middleware
  │
  ▼
Controllers
  │
  ▼
Schemas
  │
  ▼
Services
  │
  ▼
Repositories
  │
  ▼
SQLAlchemy Models
  │
  ▼
PostgreSQL
```

This architecture keeps HTTP handling, business logic, validation, database access, and authentication concerns separated.

---

## 2. Features

### Authentication

* User registration
* User login
* JWT access tokens
* JWT refresh tokens
* Protected endpoints
* Token expiration handling
* Inactive-user protection

### Authorization

Role-Based Access Control (RBAC):

* Admin
* Manager
* Employee

Authorization is enforced at the API endpoint and resource-ownership level.

### Employee Management

* Create employee
* Get employee by ID
* Get all employees
* Update employee
* Delete employee
* Employee ownership checking

### API Quality

* API versioning
* Request validation
* Standardized JSON responses
* HTTP status codes
* Pagination
* Search
* Filtering

### Documentation

* OpenAPI/Swagger UI
* API endpoint documentation
* Request/response examples
* Authentication documentation

### Testing

* Pytest
* Authentication tests
* Authorization tests
* Employee CRUD tests
* Validation tests
* Ownership tests
* Error-condition tests

---

## 3. Technology Stack

| Technology         | Purpose                       |
| ------------------ | ----------------------------- |
| Python             | Backend programming           |
| Flask              | REST API framework            |
| Flask-SQLAlchemy   | ORM/database integration      |
| SQLAlchemy         | Database abstraction          |
| PostgreSQL         | Relational database           |
| Flask-JWT-Extended | JWT authentication            |
| Flasgger           | Swagger/OpenAPI documentation |
| Pytest             | Automated testing             |
| Postman            | API testing                   |
| Git/GitHub         | Version control               |

---

## 4. Project Structure

```text
employee-management-api/
│
├── app/
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── controllers/
│   │   ├── user_controller.py
│   │   └── employee_controller.py
│   │
│   ├── middleware/
│   │   ├── auth.py
│   │   └── error_handler.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── employee.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── employee_repository.py
│   │
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── auth_routes.py
│   │   └── employee_routes.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── employee_schema.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── employee_service.py
│   │
│   ├── utils/
│   │   ├── password.py
│   │   └── response.py
│   │
│   └── __init__.py
│
├── docs/
│   └── api.md
│
├── tests/
│   ├── test_user.py
│   ├── test_auth.py
│   └── test_employee.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

## 5. Architecture

The project follows a layered architecture.

### Routes

Responsible for:

* URL definitions
* HTTP methods
* Authentication/authorization decorators
* Connecting endpoints to controllers

Example:

```text
POST /api/v1/employees
```

---

### Middleware

Responsible for cross-cutting concerns such as:

* JWT verification
* Role verification
* Error handling

---

### Controllers

Responsible for:

* Reading HTTP requests
* Calling schemas
* Calling services
* Returning HTTP responses

Controllers do not contain database logic.

---

### Schemas

Responsible for:

* Request validation
* Required fields
* Data types
* Input constraints

---

### Services

Responsible for:

* Business logic
* Duplicate checking
* Ownership rules
* Employee creation/update logic

---

### Repositories

Responsible for:

* Database queries
* Creating records
* Updating records
* Deleting records
* Retrieving records

---

### Models

Represent database tables using SQLAlchemy ORM.

Main models:

```text
User
Employee
```

---

## 6. Database Design

### User

```text
users
│
├── id
├── username
├── email
├── password_hash
├── role
├── is_active
├── created_at
└── updated_at
```

### Employee

```text
employees
│
├── id
├── user_id
├── employee_code
├── first_name
├── last_name
├── email
├── phone
├── designation
├── salary
├── joining_date
├── department
├── is_active
├── created_at
└── updated_at
```

### Relationship

Each user can have one employee record:

```text
User
 │
 │ 1 : 1
 │
 ▼
Employee
```

The relationship is implemented through:

```text
employees.user_id → users.id
```

---

## 7. Role-Based Access Control

The API uses three roles.

| Operation          | Admin | Manager |   Employee |
| ------------------ | ----: | ------: | ---------: |
| Create employee    |   Yes |     Yes |         No |
| View all employees |   Yes |     Yes |         No |
| View employee      |   Yes |     Yes | Own record |
| Update employee    |   Yes |     Yes | Own record |
| Delete employee    |   Yes |      No |         No |

Employee-level ownership is also checked.

For example:

```text
Employee A
    │
    └── Can access Employee A's record

Employee A
    │
    └── Cannot access Employee B's record
```

---

## 8. API Version

The API currently uses:

```text
/api/v1
```

Example:

```text
/api/v1/employees
```

Versioning allows future API versions to be introduced without immediately breaking existing clients.

---

# 9. API Endpoints

## Authentication

### Register

```http
POST /api/v1/users/register
```

Request:

```json
{
    "username": "employee1",
    "email": "employee1@example.com",
    "password": "Employee123"
}
```

---

### Login

```http
POST /api/v1/users/login
```

Request:

```json
{
    "username": "employee1",
    "password": "Employee123"
}
```

Response:

```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "access_token": "<access-token>",
        "refresh_token": "<refresh-token>",
        "user": {
            "id": 1,
            "username": "employee1",
            "email": "employee1@example.com",
            "role": "Employee"
        }
    }
}
```

---

### Current User

```http
GET /api/v1/users/me
```

Requires:

```text
Authorization: Bearer <access_token>
```

---

### Refresh Access Token

```http
POST /api/v1/auth/refresh
```

Requires a valid refresh token.

---

# 10. Employee API

## Create Employee

```http
POST /api/v1/employees
```

Access:

```text
Admin
Manager
```

Request:

```json
{
    "user_id": 1,
    "employee_code": "EMP001",
    "first_name": "Muhammad",
    "last_name": "Yousaf",
    "email": "employee@example.com",
    "phone": "+923001234567",
    "designation": "Software Engineer",
    "salary": 150000,
    "joining_date": "2026-09-22",
    "department": "IT",
    "is_active": true
}
```

---

## Get All Employees

```http
GET /api/v1/employees
```

Access:

```text
Admin
Manager
```

---

## Pagination

```http
GET /api/v1/employees?page=1&per_page=10
```

Response structure:

```json
{
    "success": true,
    "data": [],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 25,
        "pages": 3,
        "has_next": true,
        "has_previous": false
    }
}
```

---

## Search Employees

```http
GET /api/v1/employees?search=Yousaf
```

Search can match employee information such as:

* First name
* Last name
* Employee code
* Email

---

## Filter by Department

```http
GET /api/v1/employees?department=IT
```

---

## Filter by Active Status

```http
GET /api/v1/employees?is_active=true
```

---

## Combine Filters

```http
GET /api/v1/employees?page=1&per_page=20&search=engineer&department=IT&is_active=true
```

---

## Get Employee

```http
GET /api/v1/employees/{employee_id}
```

Example:

```http
GET /api/v1/employees/1
```

---

## Update Employee

```http
PUT /api/v1/employees/{employee_id}
```

Example:

```json
{
    "designation": "Senior Backend Developer",
    "salary": 180000,
    "department": "Engineering"
}
```

---

## Delete Employee

```http
DELETE /api/v1/employees/{employee_id}
```

Access:

```text
Admin
```

---

# 11. Authentication

Protected endpoints require a JWT access token.

Header:

```http
Authorization: Bearer <access_token>
```

Example:

```text
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

### Token Types

The application uses:

```text
Access Token
    │
    └── Short-lived API authentication

Refresh Token
    │
    └── Used to obtain a new access token
```

Current configuration:

```text
Access Token: 15 minutes
Refresh Token: 30 days
```

---

# 12. HTTP Status Codes

| Status | Meaning                          |
| -----: | -------------------------------- |
|    200 | Successful request               |
|    201 | Resource created                 |
|    400 | Invalid request/validation error |
|    401 | Authentication required/invalid  |
|    403 | Insufficient permissions         |
|    404 | Resource not found               |
|    405 | Method not allowed               |
|    409 | Resource conflict                |
|    500 | Internal server error            |

---

# 13. Error Response Format

Example:

```json
{
    "success": false,
    "message": "Insufficient permissions"
}
```

Validation example:

```json
{
    "success": false,
    "errors": {
        "email": "Invalid email address",
        "password": "Password must contain at least 8 characters"
    }
}
```

---

# 14. Swagger / OpenAPI

Interactive API documentation is available through Swagger UI.

After starting the application:

```text
http://127.0.0.1:5000/apidocs/
```

Swagger provides an interactive interface for:

* Viewing endpoints
* Inspecting request parameters
* Sending API requests
* Testing authentication-protected endpoints
* Viewing API responses

---

# 15. Installation

## Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd employee-management-api
```

---

## Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

---

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 16. PostgreSQL Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE employee_management;
```

Make sure PostgreSQL is running.

---

# 17. Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/employee_management

SECRET_KEY=your-secret-key

JWT_SECRET_KEY=your-jwt-secret-key
```

Do not commit `.env` to GitHub.

---

# 18. Database Initialization

During development, database tables can be created using:

```python
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
```

For production database schema management, migration tooling such as Flask-Migrate/Alembic should be used.

---

# 19. Running the Application

Start the API:

```powershell
python run.py
```

The development server runs at:

```text
http://127.0.0.1:5000
```

Swagger:

```text
http://127.0.0.1:5000/apidocs/
```

---

# 20. Testing

The project uses Pytest.

Run all tests:

```powershell
pytest -v
```

Run authentication tests:

```powershell
pytest tests/test_auth.py -v
```

Run employee tests:

```powershell
pytest tests/test_employee.py -v
```

The test suite covers areas including:

* User registration
* Login
* JWT authentication
* Refresh tokens
* Protected routes
* RBAC
* Employee creation
* Employee retrieval
* Employee update
* Employee deletion
* Ownership authorization
* Validation
* Duplicate records
* Not-found responses
* Pagination validation

---

# 21. API Testing with Postman

Recommended testing flow:

```text
1. Register user
       ↓
2. Login
       ↓
3. Copy access token
       ↓
4. Authorize protected requests
       ↓
5. Create employee
       ↓
6. Get employees
       ↓
7. Get employee
       ↓
8. Update employee
       ↓
9. Delete employee
```

Protected requests use:

```text
Authorization
    ↓
Bearer Token
    ↓
<access_token>
```

---

# 22. Development Workflow

The project was developed incrementally through sprints.

### Sprint 0 — Project Setup

* Python environment
* Flask setup
* Project structure
* Git

### Sprint 1 — Database Foundation

* SQLAlchemy
* PostgreSQL
* Database configuration
* Models

### Sprint 2 — User Management

* User model
* Registration
* Password hashing
* Login

### Sprint 3 — Authentication & Authorization

* JWT
* Access tokens
* Refresh tokens
* RBAC
* Protected routes

### Sprint 4 — Employee Management

* Employee model
* Employee CRUD
* Ownership authorization
* Validation
* Automated tests

### Sprint 6 — API Quality

* API versioning
* Pagination
* Search
* Filtering
* Swagger/OpenAPI
* Standardized responses
* API documentation

---

# 23. Example API Workflow

```text
                  ┌─────────────┐
                  │   Register  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │    Login    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  JWT Token  │
                  └──────┬──────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Employee APIs          User APIs
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
     Create  Read   Update
                     │
                     ▼
                   Delete
```

---

# 24. Security Considerations

The API currently implements:

* Password hashing
* JWT authentication
* Role-based authorization
* Ownership authorization
* Token expiration
* Inactive-user checks
* Input validation
* Protected endpoints
* Environment-based secrets

Secrets such as:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET_KEY
```

should be stored outside source control.

---

# 25. Future Improvements

Potential future enhancements include:

* Flask-Migrate/Alembic
* Docker
* Production WSGI server
* Structured logging
* Audit logging
* Rate limiting
* Token revocation/blacklisting
* More comprehensive automated tests
* CI/CD
* PostgreSQL production deployment
* Advanced API filtering
* Department entity and relationships
* Redis caching
* Background jobs

---

# 26. Current Project Status

```text
Project: Employee Management API

Status: Active Development

Completed:

[x] Flask REST API
[x] PostgreSQL integration
[x] SQLAlchemy ORM
[x] Layered architecture
[x] User management
[x] Password hashing
[x] JWT authentication
[x] Refresh tokens
[x] Role-based access control
[x] Employee CRUD
[x] Ownership authorization
[x] Request validation
[x] Pagination
[x] Search
[x] Filtering
[x] API versioning
[x] Swagger/OpenAPI
[x] Pytest
[x] Postman API testing

Planned:

[ ] Security hardening
[ ] Audit logging
[ ] Database migrations
[ ] Docker
[ ] Production deployment
[ ] CI/CD
```

---

## 27. Author

**Muhammad Yousaf Iqbal**

Python Backend Developer | Data & Automation | Systems Engineering

GitHub: `https://github.com/Engr-Yousuf-Iqbal`

---

## 28. License

This project is intended as a portfolio and learning project.

Add an appropriate open-source license if the repository will be distributed publicly.
