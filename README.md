# FlyRank AI Backend

A task-management REST API built with **FastAPI**, backed by a real **PostgreSQL** database, fully containerized with **Docker Compose**. One command starts everything — the API and its own database server.

## What is this?

- A complete CRUD API for tasks: create, list, fetch one, update, delete.
- The storage layer has evolved over three stages, while the API itself stayed the same:
  1. **Assignment 1** — in-memory Python list (data died on every restart)
  2. **Assignment 2** — SQLite file on disk (`tasks.db`)
  3. **This stage** — PostgreSQL running as a proper database server inside Docker
- On startup the app connects using `DATABASE_URL`, creates the `tasks` table if it does not exist, and seeds 3 example tasks — but only if the table is empty, so restarts never duplicate them.

## Run everything with one command

```
docker compose up
```

(add `-d` to run in the background: `docker compose up -d`)

What happens on the very first run:

1. Builds the `api` image from the `Dockerfile`.
2. Starts the `db` service (`postgres:17`) with a named volume, so data survives restarts.
3. Waits until Postgres passes its health check, then starts the API.
4. Creates the `tasks` table and seeds 3 example tasks (first run only).

Once running:

- Swagger UI (interactive docs): http://localhost:8000/docs
- API base: http://localhost:8000
- Health check: http://localhost:8000/health

To stop: `docker compose down` — containers are removed but the volume keeps your data. Start again with `docker compose up` and everything is still there.

## Environment variables

The app reads its database connection from `DATABASE_URL`. Copy `.env.example` to `.env` and fill in real values:

```
DATABASE_URL=postgres://user:password@localhost:5433/dbname
```

- `.env` holds real secrets and is **git-ignored** — it is never committed.
- `.env.example` holds the same keys with placeholder values and **is** committed, so anyone cloning the repo knows which variables to set.
- Inside the Compose network the API reaches the database by service name (`db`, port 5432) — this is set automatically in `compose.yaml`. From your host machine (GUI tools, psql) use `localhost:5433`.

## API Endpoints

| Method | Endpoint          | Purpose                       | Success Response |
|--------|-------------------|-------------------------------|------------------|
| POST   | `/tasks`          | Create a new task             | `201 Created`    |
| GET    | `/tasks`          | List all tasks                | `200 OK`         |
| GET    | `/tasks/{id}`     | Fetch a single task by id     | `200 OK`         |
| PUT    | `/tasks/{id}`     | Update a task                 | `200 OK`         |
| DELETE | `/tasks/{id}`     | Delete a task                 | `204 No Content` |

Validation: missing or empty `title` returns `400 Bad Request`; unknown ids return `404 Not Found` with `{ "error": "Task not found" }`.

## Example request

```
$ curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
date: Mon, 24 Aug 2026 02:50:29 GMT
server: uvicorn
content-length: 731
content-type: application/json

{"items":[{"id":1,"title":"Learn FastAPI","done":false,"created_at":"2026-08-23T12:03:09.722062+00:00","updated_at":"2026-08-23T12:03:09.722062+00:00"},{"id":2,"title":"Build a CRUD API","done":true,"created_at":"2026-08-23T12:03:09.722062+00:00","updated_at":"2026-08-23T12:03:09.722062+00:00"},{"id":3,"title":"Switch to SQLite","done":false,"created_at":"2026-08-23T12:03:09.722062+00:00","updated_at":"2026-08-23T12:03:09.722062+00:00"},{"id":4,"title":"Compose task one","done":false,"created_at":"2026-08-23T12:03:49.780096+00:00","updated_at":"2026-08-23T12:03:49.780109+00:00"},{"id":5,"title":"Compose task two","done":true,"created_at":"2026-08-23T12:03:49.989809+00:00","updated_at":"2026-08-23T12:03:49.989827+00:00"}]}
```

## Looking at the data

Open a SQL prompt straight inside the database container:

```
docker exec -it flyrank_ai_backend-db-1 psql -U postgres -d tasks
```

`\dt` — list of relations:

```
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | tasks | table | postgres
(1 row)
```

`SELECT id, title, done, created_at FROM tasks ORDER BY id;`

```
 id |      title       | done |          created_at
----+------------------+------+-------------------------------
  1 | Learn FastAPI    | f    | 2026-08-23 12:03:09.722062+00
  2 | Build a CRUD API | t    | 2026-08-23 12:03:09.722062+00
  3 | Switch to SQLite | f    | 2026-08-23 12:03:09.722062+00
  4 | Compose task one | f    | 2026-08-23 12:03:49.780096+00
  5 | Compose task two | t    | 2026-08-23 12:03:49.989809+00
(5 rows)
```

![Database Screenshot](screenshot.png)

>(connect with host `localhost`, port `5433`, user `postgres`, password `dev`, database `tasks`).

## A Note on Changing the Table Structure (Database Migrations)

When we added the `created_at` and `updated_at` columns, `CREATE TABLE IF NOT EXISTS` alone was not enough — the table already existed with real data, so we had to write extra migration code (`ALTER TABLE` + backfilling the old rows) to safely change its shape. It was a good reminder of why real-world development relies on Database Migrations: schema changes are handled explicitly and safely, so existing data is never lost and every environment ends up with the correct structure.

---

# SQL Query: Stage 4

### 1. `SELECT * FROM tasks;`

| id | title            | done |
|----|------------------|------|
| 1  | Learn FastAPI    | 0    |
| 2  | Build a CRUD API | 1    |
| 3  | Switch to SQLite | 0    |

### 2. `SELECT * FROM tasks WHERE done = 1;`

| id | title            | done |
|----|------------------|------|
| 2  | Build a CRUD API | 1    |

### 3. `SELECT COUNT(*) FROM tasks;`

| COUNT(*) |
|----------|
| 3        |

---
