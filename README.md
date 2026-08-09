# FlyRank AI Backend

## Why SQLite?

We chose **SQLite** for this project because:

- **Single file** — The entire database lives in one small file (`tasks.db`). There is no separate database server (like MySQL or PostgreSQL) to install or run. If Python is on the machine, SQLite is already there — `sqlite3` ships with Python, so nothing extra needs to be installed.
- **Data survives restarts** — In Assignment 1, data was stored in memory, so every time the server restarted, all tasks disappeared. Now data is saved to disk, so the same tasks come back after a restart. That single change — memory to disk — is what turns this project from a demo into something real.
- **Lightweight and fast** — It is perfect for small projects, learning, and single-user applications. When you need very large data or multiple users/servers, you can later move to a bigger database like Postgres.

## Where is the database file?

- The database file **`tasks.db`** lives in the project's **root directory**.
- It is **created automatically** the first time the app runs — when the code calls `sqlite3.connect("tasks.db")` and the file does not exist yet, SQLite creates it on its own.
- The `tasks` table and the seed data (3 example tasks) are also created/inserted automatically on startup. Seeding only runs when the table is empty, so restarts never duplicate the tasks.
- The file is listed in **`.gitignore`**, so it is never committed to the repository. Every fresh clone starts clean — the database is not created from someone's commit, it is created by the app itself when it runs. (Git stores code, not data.)

## How to run the project

Run this command from the project directory:

```
uvicorn main:app --reload
```

- `main:app` — the `app` (FastAPI instance) inside the `main.py` file.
- `--reload` — the server restarts automatically whenever you change the code (handy for development).
- Once the server is running:
  - API base: `http://127.0.0.1:8000`
  - Swagger UI (interactive docs): `http://127.0.0.1:8000/docs`
  - Health check: `http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint          | Purpose                       | Success Response |
|--------|-------------------|-------------------------------|------------------|
| POST   | `/tasks`          | Create a new task             | `201 Created`    |
| GET    | `/tasks`          | List all tasks                | `200 OK`         |
| GET    | `/tasks/{id}`     | Fetch a single task by id     | `200 OK`         |
| PUT    | `/tasks/{id}`     | Update a task                 | `200 OK`         |
| DELETE | `/tasks/{id}`     | Delete a task                 | `204 No Content` |

## Screenshot
![Database Screenshot](screenshot.png)


# SQL Query: Stage 4

1. SELECT * FROM tasks;

id,title,done
1,Learn FastAPI,0
2,Build a CRUD API,1
3,Switch to SQLite,0

2. SELECT * FROM tasks WHERE done = 1;

id,title,done
2,Build a CRUD API,1

3. SELECT COUNT(*) FROM tasks;

COUNT(*)
3

---
