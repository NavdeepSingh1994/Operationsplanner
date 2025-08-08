import sqlite3
import os

DB_PATH = os.path.join("db", "incidents.db")  # Wir nutzen dieselbe DB

def init_task_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            responsible TEXT,
            soll_date TEXT,
            ist_date TEXT,
            status TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, responsible, soll_date, ist_date, status, notes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, responsible, soll_date, ist_date, status, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, responsible, soll_date, ist_date, status, notes))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows
