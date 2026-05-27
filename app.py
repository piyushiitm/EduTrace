from flask import Flask, render_template, request, session, send_file
import sqlite3
import os
import hashlib
#from blockchain import AddCertificateToBlockchain

app = Flask(__name__)
app.secret_key = "EduTrace"

@app.route("/")
def home():
    return render_template("HomePage.html")

@app.route("/studentlogin")
def student():
    return render_template("LoginPages/StudentLogin.html")

@app.route("/authoritylogin")
def authority():
    return render_template("LoginPages/AuthorityLogin.html")

@app.route("/adminlogin")
def admin():
    return render_template("LoginPages/AdminLogin.html")

@app.route("/validationdashboard")
def validation():
    return render_template("Dashboards/ValidationDashboard.html")

@app.route("/admindashboard", methods=["POST"])
def adminlogin():
    username = request.form["username"]
    password = request.form["password"]
    dbconn = sqlite3.connect("Databases/Credentials/AdminCred.db")
    cursor = dbconn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username=? AND password=?",(username, password))
    admin = cursor.fetchone()
    if admin:
        return render_template("Dashboards/AdminDashboard.html")
    else:
        return render_template("LoginPages/AdminLogin.html",error="Invalid Credentials")

@app.route("/authoritydashboard", methods=["POST"])
def authoritylogin():

    username = request.form["username"]
    password = request.form["password"]

    dbconn = sqlite3.connect("DataBases/Credentials/AuthCred.db")

    cursor = dbconn.cursor()

    cursor.execute(
        "SELECT * FROM authorities WHERE username=? AND password=?",
        (username, password)
    )

    auth = cursor.fetchone()

    if auth:

        session["crrAuth"] = username

        dbconn = sqlite3.connect("DataBases/Credentials/StuCred.db")

        cursor = dbconn.cursor()

        cursor.execute(
            "SELECT username, authority FROM students WHERE authority=?",
            (username,)
        )

        students = cursor.fetchall()

        dbconn.close()

        return render_template(
            "Dashboards/AuthorityDashboard.html",
            students=students
        )

    else:

        return render_template(
            "LoginPages/AuthorityLogin.html",
            error="Invalid Credentials"
        )
    
@app.route("/studentdashboard", methods=["POST"])
def studentlogin():

    username = request.form["username"]
    password = request.form["password"]

    dbconn = sqlite3.connect("Databases/Credentials/StuCred.db")

    cursor = dbconn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE username=? AND password=?",
        (username, password)
    )

    student = cursor.fetchone()

    dbconn.close()

    if student:

        session["username"] = username

        dbconn = sqlite3.connect("Databases/Data/StuData.db")

        cursor = dbconn.cursor()

        cursor.execute(
            f"SELECT certificate, certlink FROM {username}"
        )

        certificates = cursor.fetchall()

        dbconn.close()

        return render_template(
            "Dashboards/StudentDashboard.html",
            certificates=certificates
        )

    else:

        return render_template(
            "LoginPages/StudentLogin.html",
            error="Invalid Credentials"
        )
    
@app.route("/addAuth",methods=["POST"])
def addAuthority():
    username = request.form["username"]
    password = request.form["password"]
    dbconn = sqlite3.connect("Databases/Credentials/AuthCred.db")
    cursor = dbconn.cursor()
    cursor.execute("""
        INSERT INTO authorities (username, password)
        VALUES (?, ?)
        """, (username, password))
    dbconn.commit()
    cursor.execute(
    "SELECT * FROM authorities WHERE username=? AND password=?",
    (username,password)
    )
    authority=cursor.fetchone()
    dbconn.close()
    dbconn = sqlite3.connect("Databases/Credentials/StuCred.db")
    cursor=dbconn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {username} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    dbconn.commit()
    dbconn.close()

    dbconn = sqlite3.connect("Databases/Data/AuthData.db")
    cursor = dbconn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {username}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
        )
    """)
    dbconn.commit()
    dbconn.close()
    return render_template("Dashboards/AdminDashboard.html", success="User Succesfully Added",authority=authority)

@app.route("/AddStudents")
def GotoAddStudent():
    return render_template("Dashboards/AuthFxns/AddStudent.html")

@app.route("/AddedStudent" , methods=["POST"])
def Addstudent():
    crrAuth=session["crrAuth"]
    username = request.form["username"]
    password = request.form["password"]
    #creating directory for the student added
    os.makedirs(
        "Certificates/" + username,
        exist_ok=True
    )
    #adding student data in authority table of student credential database
    dbconn = sqlite3.connect("Databases/Credentials/StuCred.db")
    cursor = dbconn.cursor()
    cursor.execute(f"""
        INSERT INTO {crrAuth} (username, password)
        VALUES (?, ?)
        """, (username, password))
    dbconn.commit()
    cursor.execute(f"""
    SELECT * FROM {crrAuth} WHERE username=? AND password=?""",
    (username,password)
    )
    student=cursor.fetchone()
    dbconn.close()
    #adding student in global table of student credential database
    dbconn = sqlite3.connect("Databases/Credentials/StuCred.db")
    cursor = dbconn.cursor()
    cursor.execute(f"""
        INSERT INTO students (username, password, authority)
        VALUES (?, ?, ?)
        """, (username, password, crrAuth))
    dbconn.commit()
    dbconn.close()
    #creating table for the student in student data database
    dbconn = sqlite3.connect("Databases/Data/StuData.db")
    cursor = dbconn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {username}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        certificate TEXT NOT NULL UNIQUE,
        certlink TEXT NOT NULL UNIQUE,
        transactionhash TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL UNIQUE
        )
    """
    )
    dbconn.commit()
    dbconn.close()
    #adding student in authority table of authdata database 
    dbconn = sqlite3.connect("Databases/Data/AuthData.db")
    cursor = dbconn.cursor()
    cursor.execute(f"""
        INSERT INTO {crrAuth} (username)
        VALUES (?)
        """, (username,))
    dbconn.commit()
    dbconn.close()
    return render_template("Dashboards/AuthorityDashboard.html", success="User Succesfully Added",student=student)

@app.route("/UploadCertificate")
def GoToUploadCertificate():
    return render_template("/Dashboards/AuthFxns/UploadCertificate.html")

@app.route("/UploadedCertificate" , methods=["POST"])
def UploadCertificate():
    crrAuth=session["crrAuth"]
    student = request.form["student"]
    certificatename = request.form["certificate"]
    certificate = request.files["CertificateFile"]
    filepath = f"""Certificates/{student}/{certificatename}.pdf"""
    certificate.save(filepath)
    #HashGeneration
    with open(filepath, "rb") as file:
        filedata = file.read()
    filehash = hashlib.sha256(filedata).hexdigest()
    #transactionhash = AddCertificateToBlockchain(
        #student,
        #crrAuth,
        #certificatename,
        #filehash
    #)
    
    dbconn = sqlite3.connect("Databases/Data/StuData.db")
    cursor = dbconn.cursor()
    cursor.execute(f"""
        INSERT INTO {student} (certificate,certlink,transactionhash,hash)
        VALUES (?,?,?,?)
    """,(certificatename, filepath,transactionhash,filehash))
    dbconn.commit()
    dbconn.close()
    return render_template("/Dashboards/AuthFxns/UploadCertificate.html" ,
                           success = f"{certificatename} succesfully uploaded for {student}")

@app.route("/ValidateDocument", methods=["POST"])
def ValidateDocument():
    document = request.files["document"]
    temppath = "temp_validation.pdf"
    document.save(temppath)
    with open(temppath, "rb") as file:
        filedata = file.read()
    generatedhash = hashlib.sha256(filedata).hexdigest()
    dbconn = sqlite3.connect("Databases/Data/StuData.db")
    cursor = dbconn.cursor()
    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)
    tables = cursor.fetchall()
    found = False
    for table in tables:
        tablename = table[0]
        try:
            cursor.execute(f"""
            SELECT transactionhash
            FROM {tablename}
            WHERE hash=?
            """, (generatedhash,))
            result = cursor.fetchone()
            if result:
                found = True
                transactionhash = result[0]
                dbconn.close()
                return render_template(
                    "Dashboards/ValidationDashboard.html",
                    success="DOCUMENT VALID"
                )
        except:
            pass
    dbconn.close()
    if not found:
        return render_template(
            "Dashboards/ValidationDashboard.html",
            error="DOCUMENT NOT FOUND / TAMPERED"
        )
    else:
        return render_template("Dashboards/ValidationDashboard.html",success="DOCUMENT is valid")
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/studentcertificates")
def studentcertificates():

    username = session.get("username")

    dbconn = sqlite3.connect("DataBases/Data/StuData.db")

    cursor = dbconn.cursor()

    cursor.execute(f"SELECT certificate, certlink FROM {username}")

    certificates = cursor.fetchall()

    dbconn.close()

    return render_template(
        "StudentCertificates.html",
        certificates=certificates
    )

@app.route("/download/<path:filepath>")
def download(filepath):

    return send_file(filepath, as_attachment=True)

