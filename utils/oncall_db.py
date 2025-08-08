import sqlite3
import os

DB_PATH = os.path.join("db", "incidents.db")

def init_oncall_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oncall (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calendar_week TEXT,
            name TEXT,
            role TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_oncall(calendar_week, name, role, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO oncall (calendar_week, name, role, email)
        VALUES (?, ?, ?, ?)
    """, (calendar_week, name, role, email))
    conn.commit()
    conn.close()

def get_all_oncalls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM oncall")
    rows = cursor.fetchall()
    conn.close()
    return rows
