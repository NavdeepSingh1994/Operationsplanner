import sqlite3
import os

DB_PATH = os.path.join("db", "incidents.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            priority TEXT,
            sla TEXT,
            teams TEXT,
            created_at TEXT,
            sent INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def create_incident(title, description, category, priority, sla, teams, created_at):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO incidents (title, description, category, priority, sla, teams, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, category, priority, sla, teams, created_at))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id
