import sqlite3

dbconn = sqlite3.connect("DataBases/Credentials/AdminCred.db")

cursor = dbconn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO admins (username, password)
VALUES (?, ?)
""", ("Piyush", "19012005"))

dbconn.commit()

dbconn.close()


dbconn = sqlite3.connect("DataBases/Credentials/StuCred.db")

cursor = dbconn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    authority TEXT NOT NULL
)
""")

dbconn.commit()

dbconn.close()

dbconn = sqlite3.connect("DataBases/Credentials/AuthCred.db")

cursor = dbconn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS authorities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password NOT NULL UNIQUE
)
""")

dbconn.commit()

dbconn.close()