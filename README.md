# FastAPI Users and Tasks Management API

A REST API built using FastAPI, SQLAlchemy, Pydantic, PostgreSQL (Supabase), JWT Authentication and Alembic.

## Features

- User registration and login
- Password hashing for secure password storage
- JWT access and refresh tokens
- Login and logout session management
- Refresh token revocation
- Teacher and Student role-based access control
- Users CRUD operations
- Tasks CRUD operations
- Assign tasks to users
- Students can view and update their own tasks
- Teachers can manage all tasks
- Task status filtering
- Task pagination
- Task search by title
- Filter tasks by assigned user
- Work notes management
- Task priority management
- Pydantic validation
- Proper HTTP error handling (401, 403, 404, 409, 422)
- Database migrations using Alembic
- Automated testing using Pytest
- Continuous Integration using GitHub Actions

## Technologies Used

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)
- SQLite (testing)
- Pydantic
- JWT
- Alembic
- Uvicorn
- Pytest
- HTTPX
- Postman
- Git and GitHub
- GitHub Actions

## Project Structure

```text
fastapi-users-api/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── users.py
│   │       └── tasks.py
│   │
│   ├── core/
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── db_models.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── async_task_service.py
│   │   └── user_service.py
│   │
│   └── main.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   └── test_users.py
│
├── alembic.ini
├── requirements.txt
├── create_teacher.py
├── reset_student_password.py
├── reset_teacher_password.py
├── README.md
└── .gitignore
```

## Database Tables

### 1. Users Table

- id
- name
- email
- phone
- password_hash
- role
- status
- created_at

### 2. Tasks Table

- id
- title
- description
- work_notes
- priority
- status
- user_id (Foreign Key)
- created_at

### 3. Sessions Table

- id
- user_id (Foreign Key)
- refresh_token_hash
- expires_at
- revoked_at
- created_at

## User Roles and Permissions

### Teacher

- Create tasks
- Assign tasks to students
- View all tasks
- Update tasks
- Delete tasks
- View users and task progress
- Filter tasks by assigned user

### Student

- View their own tasks
- Update their own task status
- Add or update work notes
- View their own profile
- Cannot assign or delete tasks
- Cannot access teacher-only information
- Cannot access other students' tasks

## Authentication Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | Logout |
| GET | `/api/v1/auth/me` | Get current user |

## Users Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/users/` | Create user |
| GET | `/api/v1/users/` | Get users |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| GET | `/api/v1/users/{user_id}/with-tasks` | Get user with tasks |
| PUT | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |

## Tasks Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/tasks/` | Create task |
| GET | `/api/v1/tasks/` | Get tasks |
| GET | `/api/v1/tasks/{task_id}` | Get task by ID |
| PUT | `/api/v1/tasks/{task_id}` | Update task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete task |

## Task Pagination, Search and Filters

The Tasks API supports pagination, searching and filtering through query parameters.

### Available Query Parameters

| Parameter | Description | Example |
|---|---|---|
| task_status | Filter tasks by status | `pending` |
| page | Page number (minimum 1) | `1` |
| limit | Number of tasks per page (1–100) | `10` |
| search | Search tasks by title | `testing` |
| assigned_user_id | Filter by assigned user (teacher only) | `2` |

### Example Requests

Get the first page with 10 tasks:

```http
GET /api/v1/tasks/?page=1&limit=10
```

Search tasks by title:

```http
GET /api/v1/tasks/?search=testing
```

Filter tasks by status:

```http
GET /api/v1/tasks/?task_status=pending
```

Filter tasks by assigned user (teacher):

```http
GET /api/v1/tasks/?assigned_user_id=2
```

Combine multiple filters:

```http
GET /api/v1/tasks/?task_status=pending&page=1&limit=5
```

Students can only access their own assigned tasks. Teachers can view and filter tasks according to their permissions.

## Task Status

Available task statuses:

- pending
- in progress
- done

## Task Priority

The tasks table includes a priority column.

Default priority:

- normal

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nidhi1709-crypto/fastapi-users-api.git
```

### 2. Open the Project Folder

```bash
cd fastapi-users-api
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment (Windows)

```powershell
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root directory.

Add the following environment variables:

```env
DATABASE_URL=your_supabase_postgresql_connection_string
JWT_SECRET_KEY=your_secure_secret_key
```

Replace the placeholder values with your own configuration.

**Important:** Never upload your `.env` file, database credentials, JWT secret keys or real passwords to GitHub.

## Database Setup

This project uses PostgreSQL hosted on Supabase.

1. Create a Supabase project.
2. Open the project's database connection settings.
3. Get the PostgreSQL connection string.
4. Add the connection string to the `.env` file.
5. Make sure the application and Alembic use the configured database.

SQLite is also configured for automated testing in GitHub Actions.

## Alembic Database Migrations

Alembic is used to manage database schema changes with SQLAlchemy.

### 1. Initialize Alembic

```bash
alembic init migrations
```

This command is required only when setting up Alembic for the first time.

### 2. Create a Migration

```bash
alembic revision --autogenerate -m "describe your changes"
```

### 3. Apply Migrations

```bash
alembic upgrade head
```

### 4. Check Current Migration

```bash
alembic current
```

### 5. View Migration History

```bash
alembic history
```

### 6. Roll Back the Last Migration

```bash
alembic downgrade -1
```

### 7. Upgrade Again

```bash
alembic upgrade head
```

### Implemented Migrations

**First Migration:**

`704f6a1df73d_create_users_tasks_and_sessions_tables.py`

- Created users table
- Created tasks table
- Created sessions table
- Added primary keys and foreign keys
- Added required columns and constraints

**Second Migration:**

`efa971e5c846_add_priority_column_to_tasks.py`

- Added priority column to the tasks table
- Used a temporary server default of `normal` for existing records
- Removed the temporary database-level default after migration

### Migration Testing

The following migration operations were tested:

1. Created the second migration using autogenerate.
2. Applied migration using `alembic upgrade head`.
3. Verified current revision using `alembic current`.
4. Rolled back using `alembic downgrade -1`.
5. Applied the migration again using `alembic upgrade head`.
6. Verified the latest migration revision.

Latest migration revision:

`efa971e5c846 (head)`

Review autogenerated migration files before applying them to the database.

## Seed Users

The project includes scripts for teacher account setup and password management.

- `create_teacher.py`
- `reset_teacher_password.py`
- `reset_student_password.py`

Use these scripts according to the project setup to create or manage test accounts.

Do not store real passwords in source code or commit them to GitHub.

## Run the Project

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

Swagger UI can be used to explore and test the API endpoints.

## Testing with Pytest

Run the automated test suite from the project root directory:

```bash
python -m pytest -v
```

The test suite covers authentication, role-based permissions, task operations and error handling.

## Testing with Postman

Test the following scenarios:

1. Teacher login
2. Student login
3. Teacher creates and assigns a task
4. Student views assigned tasks
5. Student updates task status
6. Student adds or updates work notes
7. Student cannot assign or delete tasks
8. Invalid login credentials
9. Request without authentication token
10. Expired or revoked token
11. Invalid input validation
12. Missing user or task record
13. Task pagination
14. Search tasks by title
15. Filter tasks by status
16. Filter tasks by assigned user (teacher)

## GitHub Actions Continuous Integration

This project uses GitHub Actions to automatically run tests.

Workflow file:

`.github/workflows/ci.yml`

The workflow runs when code is pushed to the `main` branch or a pull request is created for `main`.

### CI Workflow Steps

1. Check out the GitHub repository.
2. Set up Python 3.13.
3. Install project dependencies.
4. Configure SQLite test database and JWT environment variable.
5. Run tests using `python -m pytest -v`.

### Check GitHub Actions Results

1. Open the GitHub repository.
2. Select the **Actions** tab.
3. Open the **FastAPI CI** workflow.
4. Check the latest workflow run.

A green check mark indicates that the workflow completed successfully. A red cross indicates that the workflow failed and its logs should be checked.

## HTTP Status Codes

| Status Code | Description |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Resource deleted successfully |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Validation error |

## GitHub Repository

https://github.com/nidhi1709-crypto/fastapi-users-api

## Author

Nidhi Limbachiya

BCA - Third Year