import sqlite3

def init_db():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            rating TEXT,
            comment TEXT
        )
    """)

    conn.commit()
    conn.close()
