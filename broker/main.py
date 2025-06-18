import os
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "tasks.db")

app = FastAPI()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, status TEXT)"
    )
    conn.commit()
    conn.close()


class Task(BaseModel):
    id: int | None = None
    description: str
    status: str = "pending"


init_db()


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO tasks (description, status) VALUES (?, ?)",
        (task.description, task.status),
    )
    conn.commit()
    task.id = cur.lastrowid
    conn.close()
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    conn = get_db()
    cur = conn.execute("SELECT id, description, status FROM tasks")
    tasks = [
        Task(id=row["id"], description=row["description"], status=row["status"])
        for row in cur.fetchall()
    ]
    conn.close()
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT id, description, status FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    conn.close()
    if row:
        return Task(id=row["id"], description=row["description"], status=row["status"])
    raise HTTPException(status_code=404, detail="Task not found")
