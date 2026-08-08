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