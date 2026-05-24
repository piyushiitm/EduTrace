from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/student")
def student():
    return render_template("student.html")

@app.route("/authority")
def authority():
    return render_template("authority.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/validator")
def validation():
    return render_template("validator.html")
if __name__ == "__main__":
    app.run(debug=True)