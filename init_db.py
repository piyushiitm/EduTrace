import sqlite3

conn = sqlite3.connect("admincred.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
INSERT INTO admins (username, password)
VALUES (?, ?)
""", ("Piyush", "19012005"))

conn.commit()

conn.close()