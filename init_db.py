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

dbconn = sqlite3.connect("DataBases/Data/StuData.db")

cursor = dbconn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    certificate_name TEXT NOT NULL,
    certificate_path TEXT NOT NULL,
    issuer TEXT NOT NULL,
    upload_date TEXT NOT NULL,
    hash TEXT NOT NULL
)
""")

dbconn.commit()

dbconn.close()