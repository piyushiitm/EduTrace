import sqlite3

dbconn = sqlite3.connect("DataBases/AdminCred.db")

cursor = dbconn.cursor()

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

dbconn.commit()

dbconn.close()


dbconn = sqlite3.connect("DataBases/StuCred.db")

cursor = dbconn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

dbconn.commit()

dbconn.close()

dbconn = sqlite3.connect("DataBases/AuthCred.db")

cursor = dbconn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS authorities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

dbconn.commit()

dbconn.close()