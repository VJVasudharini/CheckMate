import sqlite3

DB_NAME = "todo.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DROP TABLE IF EXISTS tasks;")

        conn.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
        """)
        conn.commit()

def add_task(title: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?);", (title,))
        conn.commit()

def list_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute(
            "SELECT id, title, done FROM tasks ORDER BY done, created_at"
        ).fetchall()

def mark_done(task_id: int, done=True):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET done=? WHERE id=?", (1 if done else 0, task_id))
        conn.commit()

def delete_task(task_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
