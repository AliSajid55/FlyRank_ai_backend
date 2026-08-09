# FlyRank AI Backend

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

## Why SQLite?

Humne is project mein **SQLite** is liye choose kiya kyunki:

- **Single file** — poori database sirf ek chhota sa file hai (`tasks.db`). Koi alag database server (jaise MySQL ya PostgreSQL) install ya run karne ki zaroorat nahi hai. Jo machine pe Python hai, usi pe SQLite chalta hai — `sqlite3` Python ke saath built-in aata hai, is liye kuch extra install nahi karna parta.
- **Data restart ke baad bhi mehfooz** — pehle (Assignment 1) data memory mein store hota tha, is liye server restart karte hi sab tasks khatam ho jate the. Ab data disk par save hota hai, is liye server restart karne ke baad bhi wohi tasks wapas milte hain. Yehi woh change hai jo project ko demo se real application banata hai.
- **Lightweight aur fast** — chhote projects, learning aur single-user applications ke liye perfect hai. Jahan bahut bada data ya multiple users/servers ki zaroorat ho, wahan aage ja ke Postgres jaise bade database pe shift kiya ja sakta hai.

## Where is the database file?

- Database file **`tasks.db`** project ki **root directory** mein hoti hai.
- Ye file **khud ba khud banti hai** jab app pehli baar run hoti hai — jab code `sqlite3.connect("tasks.db")` karta hai aur file exist nahi hoti, SQLite usay automatically create kar deta hai.
- Table (`tasks`) aur seed data (3 example tasks) bhi app ke startup par automatically ban/daale jate hain — seed sirf tab chalta hai jab table khali ho, is liye restart karne se tasks duplicate nahi hote.
- Ye file **`.gitignore`** mein add ki gayi hai, is liye ye git repository mein commit nahi hoti. Har naye clone par fresh start milta hai — DB kisi ke commit karne se nahi banti, balki app chalate hi khud ban jati hai. (Git mein sirf code jata hai, data nahi.)

## How to run the project

Server start karne ke liye project directory mein ye command chalayein:

```
uvicorn main:app --reload
```

- `main:app` — `main.py` file ke andar wala `app` (FastAPI instance).
- `--reload` — jab bhi code mein change karo, server khud restart ho jata hai (development ke liye asaan).
- Server start hone ke baad:
  - API base: `http://127.0.0.1:8000`
  - Swagger UI (interactive docs): `http://127.0.0.1:8000/docs`
  - Health check: `http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint          | Purpose                            | Success Response |
|--------|-------------------|------------------------------------|------------------|
| POST   | `/tasks`          | Naya task create karein            | `201 Created`    |
| GET    | `/tasks`          | Saare tasks list karein            | `200 OK`         |
| GET    | `/tasks/{id}`     | Ek specific task id se karein      | `200 OK`         |
| PUT    | `/tasks/{id}`     | Kisi task ko update karein         | `200 OK`         |
| DELETE | `/tasks/{id}`     | Kisi task ko delete karein         | `204 No Content` |

## Screenshot

Neeche DB Browser ya VS Code SQLite extension mein khuli hui `tasks.db` ki tasveer hai (3 tasks wali table):

![Database Screenshot](screenshot.png)

> Note: `screenshot.png` naam ki file root directory mein rakh dein, ya is link ko apne screenshot ke naam se replace kar dein.
