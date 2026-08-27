# FlyRank AI Backend

A task-management REST API built with **FastAPI**, backed by **PostgreSQL**, secured with **Supabase Auth**, and fully containerized with **Docker Compose**.

## Features

- Full CRUD for tasks (create, list, get, update, delete)
- Email/password authentication via Supabase (signup, login, logout)
- Token-based route protection with a reusable dependency guard
- Swagger UI with interactive "Authorize" padlock for testing protected routes
- PostgreSQL running as a Docker service with persistent storage
- Automatic table creation and seed data on first run

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/AliSajid55/FlyRank_ai_backend.git
cd FlyRank_ai_backend
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your Supabase credentials:

```
DATABASE_URL=postgres://user:password@localhost:5433/dbname
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your_publishable_anon_key
```

> **Note:** `.env` contains real secrets and is **never committed** to Git. Only `.env.example` (with placeholder values) is tracked.

### 3. Run everything with one command

```bash
docker compose up
```

Add `-d` to run in the background: `docker compose up -d`

What happens on first run:

1. Builds the API image from the `Dockerfile`
2. Starts PostgreSQL 17 with a named volume (data survives restarts)
3. Waits for the database health check to pass, then starts the API
4. Creates the `tasks` table and seeds 3 example tasks (first run only)

### 4. Open Swagger UI

Navigate to **http://localhost:8000/docs** to see the interactive API documentation.

## API Reference

### Public Endpoints (no auth required)

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Root message | `200` |
| `GET` | `/health` | Health check | `200` |
| `GET` | `/public/info` | Public info | `200` |

### Auth Endpoints

| Method | Endpoint | Description | Auth | Response |
|--------|----------|-------------|------|----------|
| `POST` | `/auth/signup` | Register a new user | No | `201` |
| `POST` | `/auth/login` | Login and get tokens | No | `200` |
| `POST` | `/auth/logout` | Logout and invalidate session | Yes | `204` |

### Protected Endpoints (Bearer token required)

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/protected/profile` | Get current user profile | `200` |
| `GET` | `/protected/dashboard` | Get dashboard with user info | `200` |

### Task Endpoints

| Method | Endpoint | Description | Auth | Response |
|--------|----------|-------------|------|----------|
| `POST` | `/tasks` | Create a new task | No | `201` |
| `GET` | `/tasks` | List all tasks | No | `200` |
| `GET` | `/tasks/{id}` | Get a single task | No | `200` |
| `PUT` | `/tasks/{id}` | Update a task | No | `200` |
| `DELETE` | `/tasks/{id}` | Delete a task | No | `204` |

## Authentication Flow

1. **Signup:** `POST /auth/signup` with `{"email": "...", "password": "..."}`
2. **Login:** `POST /auth/login` to receive an `access_token`
3. **Access protected routes:** Pass the token in the `Authorization` header:
   ```
   Authorization: Bearer <your_access_token>
   ```
4. **Logout:** `POST /auth/logout` with the same header to invalidate the session

## Testing with Swagger UI

1. Go to **http://localhost:8000/docs**
2. Click the green **Authorize** button at the top
3. Paste your `access_token` (from login) into the value field and click **Authorize**
4. All protected endpoints now have a padlock icon — use **Try it out** to test them

## Project Structure

```
.
├── main.py                 # FastAPI app, routes, and task CRUD
├── auth.py                 # Authentication routes (signup, login, logout)
├── dependencies.py         # Reusable token verification dependency
├── repository.py           # PostgreSQL database operations
├── supabase_client.py      # Supabase client initialization
├── requirements.txt        # Python dependencies
├── Dockerfile              # API container image
├── compose.yaml            # Docker Compose (API + PostgreSQL)
├── .env.example            # Environment variable template
└── .gitignore              # Git ignore rules
```

## Stopping

```bash
docker compose down
```

Containers are removed but the database volume persists. Run `docker compose up` again and your data is still there.

## Tech Stack

- **Backend:** FastAPI (Python 3.14)
- **Database:** PostgreSQL 17
- **Auth:** Supabase
- **Containerization:** Docker + Docker Compose
- **API Docs:** Swagger UI (auto-generated)
