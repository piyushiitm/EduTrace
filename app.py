from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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
    dbconn = sqlite3.connect("Databases/AdminCred.db")
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
    dbconn = sqlite3.connect("Databases/AuthCred.db")
    cursor = dbconn.cursor()
    cursor.execute("SELECT * FROM authorities WHERE username=? AND password=?",(username, password))
    auth = cursor.fetchone()
    if auth :
        return render_template("Dashboards/AuthorityDashboard.html")
    else:
        return render_template("LoginPages/AuthorityLogin.html",error="Invalid Credentials")
    
@app.route("/studentdashboard", methods=["POST"])
def studentlogin():
    username = request.form["username"]
    password = request.form["password"]
    dbconn = sqlite3.connect("StuCred.db")
    cursor = dbconn.cursor()
    cursor.execute("SELECT * FROM students WHERE username=? AND password=?",(username, password))
    student = cursor.fetchone()
    if student :
        return render_template("Dashboards/StudentDashboard.html")
    else:
        return render_template("LoginPages/StudentLogin.html",error="Invalid Credentials")

@app.route("/addAuth",methods=["POST"])
def addAuthority():
    username = request.form["username"]
    password = request.form["password"]
    dbconn = sqlite3.connect("Databases/AuthCred.db")
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
    return render_template("Dashboards/AdminDashboard.html", success="User Succesfully Added",authority=authority)

if __name__ == "__main__":
    app.run(debug=True)